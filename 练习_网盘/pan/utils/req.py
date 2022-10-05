import os
import struct

"""
处理收发数据以及收发文件的粘包问题
"""

def send_data(conn, content):
    """ 发送数据 """
    data = content.encode('utf-8')
    header = struct.pack("i", len(data))
    conn.sendall(header)
    conn.sendall(data)

def recv_data(conn):
    """ 接受数据"""
    # 获取数据长度
    has_read_size = 0
    bytes_list = []
    while has_read_size < 4:
        chunk = conn.recv(4 - has_read_size)
        has_read_size += len(chunk)
        bytes_list.append(chunk)
    header = b"".join(bytes_list)
    data_length = struct.unpack("i", header)[0]

    # 获取数据
    data = b""
    has_read_size = 0
    while has_read_size < data_length:
        length = data_length - has_read_size
        if length > 1024:
            lth = 1024
        else:
            lth = length
        chunk = conn.recv(lth)
        data += chunk
        has_read_size += len(chunk)
    return data

def recv_save_file(conn, save_file_path):
    """ 接受并且保存文件"""
    # 获取头部信息：数据长度
    has_recv_size = 0
    bytes_list = []
    while has_recv_size < 4:
        chunk = conn.recv(4 - has_recv_size)
        bytes_list.append(chunk)
        has_recv_size += len(chunk)
    header = b"".join(bytes_list)
    data_length = struct.unpack("i", header)[0]

    # 获取数据
    file_ob = open(save_file_path, mode="wb")
    has_read_size = 0
    while has_read_size < data_length:
        length = data_length - has_read_size
        if length > 1024:
            lth = 1024
        else:
            lth = length
        chunk = conn.recv(lth)
        file_ob.write(chunk)
        file_ob.flush()
        has_read_size += len(chunk)
    file_ob.close()


def send_file_by_seek(conn, file_size, file_path, seek=0):
    """ 读取并发送文件（支持从指定字节位置开始读取） """
    header = struct.pack("i", file_size)
    conn.sendall(header)

    has_send_size = 0
    file_object = open(file_path, mode="rb")
    if seek:
        file_object.seek(seek)
    while has_send_size < file_size:
        chunk = file_object.read(2048)
        conn.sendall(chunk)
        has_send_size += len(chunk)
    file_object.close()




