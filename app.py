# script: app.py
from flask import Flask, jsonify, send_from_directory
import xml.etree.ElementTree as ET
from flask_cors import CORS
from lxml import etree
import os
import re

app = Flask(__name__, static_folder='static')
CORS(app)

def validate_xml(xml_file, xsd_file):
    with open(xsd_file, 'rb') as schema_file:
        schema_root = etree.XML(schema_file.read())
        schema = etree.XMLSchema(schema_root)
        parser = etree.XMLParser(schema=schema)
        try:
            with open(xml_file, 'rb') as xml:
                etree.fromstring(xml.read(), parser)
            return True, None
        except etree.XMLSyntaxError as e:
            return False, str(e)
        except etree.DocumentInvalid as e:
            return False, str(e.error_log)

def parse_sql_comments(sql_file):
    comments = {}
    with open(sql_file, 'r') as file:
        sql_content = file.read()
        matches = re.findall(r"VALUES\('([^']*)',\d+,\d+,\w+,'',\d+,'([^']*)'", sql_content)
        for guid, comment in matches:
            try:
                # Parse the comment content
                comment_data = parse_comment_content(comment)
                comments[guid] = comment_data
            except ET.ParseError as e:
                print(f"Error parsing comment for GUID {guid}: {e}")
    return comments

def parse_comment_content(comment):
    try:
        # Parse the XML content of the comment
        root = ET.fromstring(comment)
        comment_data = {
            'GUID': root.get('GUID'),
            'id': root.get('id'),
            'order': root.get('order'),
            'isValid': root.get('isValid'),
            'validDate': root.get('validDate'),
            'version': root.get('version'),
            'article': root.get('article'),
            'formatUnits': []
        }
        for format_unit in root.findall('formatUnit'):
            format_unit_data = {attr: format_unit.get(attr) for attr in format_unit.keys()}
            format_unit_data['text'] = format_unit.text
            comment_data['formatUnits'].append(format_unit_data)
        return comment_data
    except ET.ParseError as e:
        print(f"Error parsing comment: {e}")
        return None

@app.route('/api/data', methods=['GET'])
def get_data():
    try:
        xml_file = os.path.join('archive', 'full', 'et.xml')
        xsd_file = os.path.join('archive', 'XMLSchema', 'LOXML.xsd')
        sql_file = os.path.join('archive', 'comentariosaj', 'et._ComentariosAj.sql')
        
        is_valid, error = validate_xml(xml_file, xsd_file)
        if not is_valid:
            return jsonify({'error': f'XML Validation Error: {error}'}), 400

        tree = ET.parse(xml_file)
        root = tree.getroot()
        
        data = parse_xml(root)

        comments = parse_sql_comments(sql_file)
        data = add_comments_to_blocks(data, comments)
        
        return jsonify({'data': data})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

def parse_xml(root):
    data = {
        'documentMetadata': {},
        'blocks': []
    }
    
    metadata = root.find('documentMetadata')
    if (metadata is not None):
        data['documentMetadata'] = {attr: metadata.get(attr) for attr in metadata.keys()}
    
    for block in root.findall('block'):
        block_data = {attr: block.get(attr) for attr in block.keys()}
        block_data['formatUnits'] = []
        
        for format_unit in block.findall('formatUnit'):
            format_unit_data = {attr: format_unit.get(attr) for attr in format_unit.keys()}
            format_unit_data['text'] = format_unit.text
            block_data['formatUnits'].append(format_unit_data)
        
        data['blocks'].append(block_data)
    
    return data

def add_comments_to_blocks(data, comments):
    for block in data['blocks']:
        guid = block.get('GUID')
        if guid and guid in comments:
            block['comments'] = [comments[guid]]
        else:
            block['comments'] = []
    return data

@app.route('/images/<path:filename>', methods=['GET'])
def serve_image(filename):
    return send_from_directory('Imagenes', filename)

@app.route('/', methods=['GET'])
def serve_react_app():
    return send_from_directory(app.static_folder, 'index.html')

@app.route('/<path:path>', methods=['GET'])
def serve_static_files(path):
    return send_from_directory(app.static_folder, path)

if __name__ == '__main__':
    app.run(debug=True)