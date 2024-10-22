from flask import Flask, send_from_directory, request
from flask_socketio import SocketIO, emit
import eventlet

eventlet.monkey_patch()

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*", async_mode='threading')

# Rota para enviar o vídeo
@app.route('/video')
def get_video():
    return send_from_directory('videos', 'sample_video.mp4')

# WebSocket: envia uma mensagem ao cliente ao conectar
@socketio.on('connect')
def handle_connect():
    emit('message', {'data': 'Conexão estabelecida!'})

# WebSocket: recebe e lida com mensagens do cliente
@socketio.on('play_video')
def handle_play_video(data):
    print(f"Reproduzindo vídeo: {data}")
    emit('start_video', {'url': '/video'})  # Envia a URL do vídeo para o cliente

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=5000, debug=True)
