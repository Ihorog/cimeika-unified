"""
CIMEIKA Backend Main Entry Point
Flask + FastAPI integration
"""
import os
from flask import Flask, jsonify, request
from flask_cors import CORS
from dotenv import load_dotenv
from app.config.canon import CANON_BUNDLE_ID, CANON_MANIFEST
from app.utils.seo_matrix import get_seo_matrix

# Load environment variables
load_dotenv()

# Initialize Flask app
app = Flask(__name__)

# Configure CORS
CORS(app, origins=os.getenv('CORS_ORIGINS', 'http://localhost:3000').split(','))

# Configuration
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev-secret-key')
app.config['DEBUG'] = os.getenv('FLASK_DEBUG', '1') == '1'

# Database configuration
app.config['SQLALCHEMY_DATABASE_URI'] = (
    f"postgresql://{os.getenv('POSTGRES_USER', 'cimeika_user')}:"
    f"{os.getenv('POSTGRES_PASSWORD', 'change_me')}@"
    f"{os.getenv('POSTGRES_HOST', 'postgres')}:"
    f"{os.getenv('POSTGRES_PORT', '5432')}/"
    f"{os.getenv('POSTGRES_DB', 'cimeika')}"
)


@app.route('/')
def index():
    """Health check endpoint"""
    return jsonify({
        'status': 'success',
        'message': 'CIMEIKA Backend API is running',
        'version': '0.1.0',
        'canon_bundle_id': CANON_BUNDLE_ID,
        'modules': [
            'Ci - Центральне ядро',
            'Казкар - Пам\'ять',
            'Подія - Події',
            'Настрій - Емоції',
            'Маля - Ідеї',
            'Галерея - Медіа',
            'Календар - Час'
        ]
    })


@app.route('/health')
def health():
    """Health check for monitoring"""
    # Note: In a production environment, you would check actual connectivity
    # to PostgreSQL and Redis here
    return jsonify({
        'status': 'healthy',
        'message': 'Backend is running',
        'canon_bundle_id': CANON_BUNDLE_ID,
        'timestamp': os.getenv('BACKEND_PORT', '5000')
    })


@app.route('/api/v1/modules')
def modules():
    """Get list of available modules"""
    return jsonify({
        'canon_bundle_id': CANON_BUNDLE_ID,
        'modules': [
            {
                'id': 'ci',
                'name': 'Ci',
                'description': 'Центральне ядро, оркестрація',
                'status': 'in_development'
            },
            {
                'id': 'kazkar',
                'name': 'Казкар',
                'description': 'Пам\'ять, історії, легенди',
                'status': 'in_development'
            },
            {
                'id': 'podiya',
                'name': 'Подія',
                'description': 'Події, майбутнє, сценарії',
                'status': 'in_development'
            },
            {
                'id': 'nastriy',
                'name': 'Настрій',
                'description': 'Емоційні стани, контекст',
                'status': 'in_development'
            },
            {
                'id': 'malya',
                'name': 'Маля',
                'description': 'Ідеї, творчість, інновації',
                'status': 'in_development'
            },
            {
                'id': 'galereya',
                'name': 'Галерея',
                'description': 'Візуальний архів, медіа',
                'status': 'in_development'
            },
            {
                'id': 'kalendar',
                'name': 'Календар',
                'description': 'Час, ритми, планування',
                'status': 'in_development'
            }
        ]
    })


@app.route('/api/v1/seo/states')
def seo_states():
    """Get all available emotional states"""
    try:
        seo_matrix = get_seo_matrix()
        states = seo_matrix.get_all_states()
        return jsonify({
            'status': 'success',
            'states': states
        })
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500


@app.route('/api/v1/seo/intents/<state>')
def seo_intents(state):
    """Get all available intents for a state"""
    try:
        seo_matrix = get_seo_matrix()
        intents = seo_matrix.get_all_intents(state)
        return jsonify({
            'status': 'success',
            'state': state,
            'intents': intents
        })
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500


@app.route('/api/v1/seo/meta/<state>/<intent>')
def seo_meta(state, intent):
    """Get SEO metadata for a specific state and intent"""
    try:
        seo_matrix = get_seo_matrix()
        data = seo_matrix.get_full_seo_data(state, intent)
        
        if not data:
            return jsonify({
                'status': 'error',
                'message': f'No SEO data found for state={state}, intent={intent}'
            }), 404
        
        return jsonify({
            'status': 'success',
            'state': state,
            'intent': intent,
            'data': data
        })
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500


@app.route('/api/v1/seo/config')
def seo_config():
    """Get SEO configuration"""
    try:
        seo_matrix = get_seo_matrix()
        return jsonify({
            'status': 'success',
            'config': {
                'canonical_lang': seo_matrix.canonical_lang,
                'hreflang_patterns': seo_matrix.hreflang_patterns,
                'rules': seo_matrix.rules
            }
        })
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500


if __name__ == '__main__':
    port = int(os.getenv('BACKEND_PORT', 5000))
    host = os.getenv('BACKEND_HOST', '0.0.0.0')
    app.run(host=host, port=port, debug=app.config['DEBUG'])
