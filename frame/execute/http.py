http_success = "HTTP/1.1 200 OK"
content_type="Content-Type: "

#html
_content_type_text=content_type+"text/html;charset=utf-8"
content_type_text="\n"+_content_type_text+"\n\n"
#纯文本
_content_type_text_plain=content_type+"text/plain;charset=utf-8"
content_type_text_plain="\n"+_content_type_text_plain+"\n\n"
#xml
_content_type_text_xml=content_type+"text/xml"
content_type_text_xml="\n"+_content_type_text_xml+"\n\n"
#：gif图片格式
_content_type_gif=content_type+"image/gif"
content_type_gif="\n"+_content_type_gif+"\n\n"
#：jpg图片格式
_content_type_jpeg=content_type+"image/jpeg"
content_type_jpeg="\n"+_content_type_jpeg+"\n\n"
#：png图片格式
_content_type_png=content_type+"image/png"
content_type_png="\n"+_content_type_png+"\n\n"
# ：XHTML格式
_content_type_xhtml=content_type+"application/xhtml+xml"
content_type_xhtml="\n"+_content_type_xhtml+"\n\n"
#： XML数据格式
_content_type_xml=content_type+"application/xml"
content_type_xml="\n"+_content_type_xml+"\n\n"
# ：Atom XML聚合格式
_content_type_atomxml=content_type+"application/atom+xml"
content_type_atomxml="\n"+_content_type_atomxml+"\n\n"
#：pdf格式
_content_type_pdf=content_type+"application/pdf"
content_type_pdf="\n"+_content_type_pdf+"\n\n"
# ： Word文档格式
_content_type_word=content_type+"application/msword"
content_type_word="\n"+_content_type_word+"\n\n"
# ： 二进制流数据（如常见的文件下载）
_content_type_stream=content_type+"application/octet-stream"
content_type_stream="\n"+_content_type_stream+"\n\n"
# ： <form encType=””>中默认的encType，form表单数据被编码为key/value格式发送到服务器（表单默认的提交数据的格式）
_content_type_form=content_type+"application/x-www-form-urlencoded"
content_type_form="\n"+_content_type_form+"\n\n"
#json
_content_type_json=content_type+"application/json;charset=utf-8"
content_type_json="\n"+_content_type_json+"\n\n"

content_type_dict={
    "html":content_type_text,
    "text":content_type_text_plain,
    "gif":content_type_gif,
    "png":content_type_png,
    "jpg":content_type_jpeg,
    "pdf":content_type_pdf,
    "word":content_type_word,
    "xml":content_type_xml
}

#服务器繁忙，服务器不可用
http_busy = '''
HTTP/1.1 503 Service Unavailable
'''.encode()

#请求资源未找到
http_notfound = '''
HTTP/1.1 404 Not Found
'''.encode()

#方法执行出现一样，请求失败
http_servererror = '''
HTTP/1.1 500 Server Error
'''.encode()

http_serverforbidden='''
HTTP/1.1 403 Forbidden
Content-Type: text/html;charset=utf-8

服务器禁止了这个请求
'''.encode()
