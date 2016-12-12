#!/usr/bin/env python
#
# oss_server.py: Web application for serving images as defined in IIIF 2.1
#                specification (http://iiif.io/api/image/2.1/)
#
# created by: Amit Verma
#
from openslide import open_slide
from flask import Flask, make_response, send_file, abort, jsonify
from io import BytesIO
import math

imagehome = '/'

class PILBytesIO(BytesIO):
    def fileno(self):
        '''Classic PIL doesn't understand io.UnsupportedOperation.'''
        raise AttributeError('Not supported')

app = Flask(__name__)

#@app.route('/')
#def hello():
#    return 'hello, world'

## Code to load test the service using loader.io
#@app.route('/loaderio-c5c2c752dcfe4b5a8aa7348188fe7012/')
#def verify():
#    return 'loaderio-c5c2c752dcfe4b5a8aa7348188fe7012'

# Image Information Request URI (IIIF 2.1 specification)
# {scheme}://{server}{/prefix}/{identifier}/info.json
@app.route('/<path:prefix>/<string:identifier>/info.json', methods = ['GET'])
def getImageInfo(prefix, identifier):
    fileloc = imagehome + prefix + '/' + identifier
    slide = open_slide(fileloc)
    dims = slide.dimensions
    info = {'@context':'http://iiif.io/api/image/2/context.json',
            '@id': prefix + identifier,
            'protocol': 'http://iiif.io/api/image',
            'width': str(dims[0]),
            'height': str(dims[1]),
            'profile': ['http://iiif.io/api/image/2/level2.json']
            }
    return jsonify(**info)


# Image Request URI (IIIF 2.1 specification)
# {scheme}://{server}{/prefix}/{identifier}/{region}/{size}/{rotation}/{quality}.{format}
# Region THEN Size THEN Rotation THEN Quality THEN Format
@app.route('/<path:prefix>/<string:identifier>/<string:region>/<string:size>/<mirror><int:rotation>/<string:qlt_fmt>', methods = ['GET'])
@app.route('/<path:prefix>/<string:identifier>/<string:region>/<string:size>/<int:rotation>/<string:qlt_fmt>', methods = ['GET'])
def getImage(prefix, identifier, region, size, rotation, qlt_fmt, mirror=None):
    fileloc = imagehome + prefix + '/' + identifier
    print(fileloc)
    try:
    	slide = open_slide(fileloc)
        dims = slide.dimensions
        # region
        roi = region.split(',')
        roi_params = len(roi)
        if (roi_params == 1):
            if (roi[0].lower() == 'full'):
                x = 0
                y = 0
                w = dims[0] - 1
                h = dims[1] - 1
            elif (roi[0].lower() == 'square'):
                if (dims[0] > dims[1]):
                    x = (dims[0] - dims[1]) / 2 - 1
                    y = 0
                    w = x + dims[1] - 1
                    h = dims[1] - 1
                else:
                    x = 0
                    y = (dims[1] - dims[0]) / 2 - 1
                    w = dims[1] - 1
                    h = y + dims[1] - 1
            else:
                abort(400)
        elif (roi_params == 4):
            first_p = roi[0].split(':')
            if (len(first_p) == 2):
                if (first_p[0] == 'pct'):
                    x = int(math.ceil(float(first_p[1]) * dims[0] / 100)) - 1
                    y = int(math.ceil(float(roi[1]) * dims[1] / 100)) - 1
                    w = int(math.ceil(float(roi[2]) * dims[0] / 100)) - 1
                    h = int(math.ceil(float(roi[3]) * dims[1] / 100)) - 1
                else:
                    abort(400)
            else:
                x = int(roi[0])
                y = int(roi[1])
                w = int(roi[2])
                h = int(roi[3])
            if (w == 0 | h == 0 | x > (dims[0] - 1) | y > (dims[1] - 1)): #check
                abort(400)
        else:
            abort(400)

        if (w > (dims[0] -1)):
            w = dims[0] - 1
        if (h > (dims[1] -1)):
            h = dims[1] - 1

        tile = slide.read_region((x,y),0,(w,h))

        # size
        if ((size == "full") | (size == "max")):
            sw = w
            sh = h
        elif (size.find(':') != -1):
            sparts = size.split(':')
            if (sparts[0] == 'pct'):
                sw = int(float(sparts[1])) * w / 100
                sh = int(float(sparts[1])) * h / 100
            else:
                abort(400)
        elif (size.find(',') != -1):
            commaInd = size.find(',')
            sparts = size.split(',')
            print("sparts:",sparts)
            print("commaInd:", commaInd)
            if (commaInd == len(size)-1):
                sw = int(sparts[0])
                sh = int(h * float(sw) / w)
            elif (commaInd == 0):
                print("inside")
                sh = int(sparts[1])
                sw = int(w * float(sh) / h)
            elif (len(sparts) == 2):
                if (size[0] == '!'):
                    sw = int(sparts[0][1:])
                    sh = int(sparts[1])
                    if (sw > w & sh > h):
                        sw = w
                        sh = h
                    elif (sw > w & sh <= h):
                        sw = int(w * float(sh) / h)
                    elif (sh > h & sw <= w):
                        sh = int(h * float(sw) / w)
                    elif (sw <= w & sh <= h):
                        sh = int(h * float(sw) / w)
                else:
                    sw = int(sparts[0])
                    sh = int(sparts[1])
            else:
                print('aa')
                abort(400)
        else:
            print('bb')
            abort(400)
        print('sw:',sw,'sh:',sh)
        tile = tile.resize((sw,sh),resample=3)

        # rotation
        if (mirror == '!'):
            tile = tile.transpose(0)
        tile = tile.rotate(rotation,expand=1)

        # quality
        qf = qlt_fmt.split('.')
        if (len(qf) != 2):
            abort(400)

        if (qf[0] == 'default'):
            tile = tile
        elif (qf[0] == 'color'):
            tile = tile.convert(mode='RGB')
        elif (qf[0] == 'gray'):
            tile = tile.convert(mode='L')
        elif (qf[0] == 'bitonal'):
            tile = tile.convert(mode='1')
        else:
            abort(400)

        # format
        if (qf[1] == 'jpg'):
            format = 'jpeg'
            mime_type = 'image/jpeg'
        elif (qf[1] == 'tif'):
            format = 'tiff'
            mime_type  = 'image/tiff'
        elif (qf[1] == 'png'):
            format = 'png'
            mime_type  = 'image/png'
        elif (qf[1] == 'gif'):
            format = 'gif'
            mime_type  = 'image/gif'
        elif (qf[1] == 'jp2'):
            format = 'jpeg2000'
            mime_type  = 'image/jp2'
            tile = tile.convert('RGB')
        elif (qf[1] == 'pdf'):
            format = 'pdf'
            mime_type = 'application/pdf'
        elif (qf[1] == 'webp'):
            format = 'webp'
            mime_type = 'image/webp'
        else:
            abort(400)

        buf = PILBytesIO()
        tile.save(buf, format)
        buf.seek(0)
        return send_file(buf, mimetype = mime_type,
        attachment_filename=qlt_fmt, as_attachment=False)

    except IOError:
        abort(404)
    except ValueError:
        abort(400)
    except RuntimeError:
        abort(500)





if __name__ == '__main__':
    app.run(host='0.0.0.0')
