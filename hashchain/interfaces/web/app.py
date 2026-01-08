"""Interface web para HashChain usando Flask."""
try:
    from flask import Flask, render_template, request, jsonify
    FLASK_AVAILABLE = True
except ImportError:
    FLASK_AVAILABLE = False
    # Não imprime mensagem aqui para não poluir o output

from hashchain import HashChain
import secrets

# Instância global do HashChain
hashchain = HashChain()

# Inicializa Flask se disponível
if FLASK_AVAILABLE:
    import os
    from pathlib import Path
    
    # Define o caminho dos templates relativo ao arquivo atual
    template_dir = Path(__file__).parent / 'templates'
    app = Flask(__name__, template_folder=str(template_dir))
    app.config['SECRET_KEY'] = secrets.token_hex(16)
    
    @app.route('/')
    def index():
        """Página principal."""
        return render_template('index.html')
    
    @app.route('/api/encrypt', methods=['POST'])
    def api_encrypt():
        """API para criptografar texto."""
        try:
            data = request.get_json()
            plaintext = data.get('plaintext', '')
            seed = data.get('seed', 0)
            passes = data.get('passes', None)
            no_salt = data.get('no_salt', False)
            
            if not plaintext:
                return jsonify({'error': 'Texto não fornecido'}), 400
            
            # Converte seed se for string
            if isinstance(seed, str):
                if seed:
                    try:
                        seed = int(seed)
                    except ValueError:
                        return jsonify({'error': 'Seed inválida'}), 400
                else:
                    seed = 0
            
            # Converte passes se for string
            if isinstance(passes, str) and passes:
                try:
                    passes = [int(x) for x in passes.split()]
                except ValueError:
                    return jsonify({'error': 'Passes inválidos'}), 400
            
            # Criptografa
            hashchain.encrypt(
                plaintext=plaintext,
                pass_=passes,
                seed=seed,
                no_salt=no_salt
            )
            
            return jsonify({
                'success': True,
                'ciphertext': hashchain.info(0),
                'key': hashchain.info(1),
                'plaintext': hashchain.info(3)
            })
        
        except Exception as e:
            return jsonify({'error': str(e)}), 500
    
    @app.route('/api/decrypt', methods=['POST'])
    def api_decrypt():
        """API para descriptografar texto."""
        try:
            data = request.get_json()
            ciphertext = data.get('ciphertext', '')
            key = data.get('key', '')
            
            if not ciphertext or not key:
                return jsonify({'error': 'Ciphertext e/ou chave não fornecidos'}), 400
            
            # Descriptografa
            hashchain.decrypt(ciphertext=ciphertext, key=key)
            
            return jsonify({
                'success': True,
                'plaintext': hashchain.info(3)
            })
        
        except Exception as e:
            return jsonify({'error': str(e)}), 500
    
    @app.route('/api/compress', methods=['POST'])
    def api_compress():
        """API para comprimir texto binário."""
        try:
            data = request.get_json()
            text = data.get('text', '')
            
            if not text:
                return jsonify({'error': 'Texto não fornecido'}), 400
            
            result = hashchain.compression(text)
            
            if result is None:
                return jsonify({'error': 'Erro ao comprimir. Verifique se o texto contém apenas 0 e 1'}), 400
            
            return jsonify({
                'success': True,
                'compressed': result
            })
        
        except Exception as e:
            return jsonify({'error': str(e)}), 500
    
    @app.route('/api/decompress', methods=['POST'])
    def api_decompress():
        """API para descomprimir texto."""
        try:
            data = request.get_json()
            compressed_text = data.get('compressed_text', '')
            
            if not compressed_text:
                return jsonify({'error': 'Texto comprimido não fornecido'}), 400
            
            result = hashchain.decompression(compressed_text)
            
            if result.startswith("Erro"):
                return jsonify({'error': result}), 400
            
            return jsonify({
                'success': True,
                'decompressed': result
            })
        
        except Exception as e:
            return jsonify({'error': str(e)}), 500
    
    @app.route('/api/generate-seed', methods=['GET'])
    def api_generate_seed():
        """Gera uma seed aleatória."""
        num_digits = secrets.randbelow(65) + 64
        seed = int("".join(str(secrets.randbelow(10)) for _ in range(num_digits)))
        return jsonify({'seed': seed})
    
    @app.route('/api/generate-passes', methods=['GET'])
    def api_generate_passes():
        """Gera passes aleatórios."""
        num_passes = secrets.randbelow(64) + 8
        passes = [secrets.randbelow(979) + 20 for _ in range(num_passes)]
        return jsonify({'passes': passes})
else:
    app = None


def run_web(host='127.0.0.1', port=5000, debug=False):
    """Inicia o servidor web."""
    if not FLASK_AVAILABLE:
        print("\n❌ Erro: Flask não está instalado!")
        print("📦 Instale com: pip install Flask")
        print("   Ou instale todas as dependências: pip install -r requirements.txt\n")
        return
    
    if app is None:
        print("\n❌ Erro: Aplicação Flask não foi inicializada corretamente!\n")
        return
    
    print(f"\n🌐 Servidor web HashChain iniciado em http://{host}:{port}")
    print(f"📝 Acesse http://{host}:{port} no seu navegador")
    print(f"🛑 Pressione Ctrl+C para parar o servidor\n")
    app.run(host=host, port=port, debug=debug)

