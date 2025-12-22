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

# Import module blueprints
from api.ci import ci_bp
from api.calendar import calendar_bp
from api.podija import podija_bp
from api.nastrij import nastrij_bp
from api.gallery import gallery_bp
from api.kazkar import kazkar_bp
from api.malya import malya_bp

# Load environment variables
load_dotenv()

# Initialize Flask app
app = Flask(__name__)

# Configure CORS
CORS(app, origins=os.getenv('CORS_ORIGINS', 'http://localhost:3000').split(','))

# Register module blueprints
app.register_blueprint(ci_bp)
app.register_blueprint(calendar_bp)
app.register_blueprint(podija_bp)
app.register_blueprint(nastrij_bp)
app.register_blueprint(gallery_bp)
app.register_blueprint(kazkar_bp)
app.register_blueprint(malya_bp)

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
    from datetime import datetime
    # Note: In a production environment, you would check actual connectivity
    # to PostgreSQL and Redis here
    return jsonify({
        'status': 'healthy',
        'message': 'Backend is running',
        'canon_bundle_id': CANON_BUNDLE_ID,
        'timestamp': datetime.utcnow().isoformat(),
        'version': '0.1.0'
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


# New comprehensive SEO endpoints using the enhanced SEO service
@app.route('/api/v1/ci/seo/v2/entry/<lang>/<state>/<intent>')
def seo_v2_entry(lang, state, intent):
    """Get comprehensive SEO entry with module mapping and writes policy"""
    try:
        from app.config.seo import seo_service
        entry = seo_service.get_entry(lang, state, intent)
        if not entry:
            return jsonify({
                'status': 'error',
                'message': f'SEO entry not found for {lang}/{state}/{intent}'
            }), 404
        return jsonify({
            'status': 'success',
            'entry': entry
        })
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500


@app.route('/api/v1/ci/seo/v2/entries/<lang>')
def seo_v2_all_entries(lang):
    """Get all comprehensive SEO entries for a language"""
    try:
        from app.config.seo import seo_service
        if lang not in seo_service.get_languages():
            return jsonify({
                'status': 'error',
                'message': f'Unsupported language: {lang}'
            }), 400
        entries = seo_service.get_all_entries(lang)
        return jsonify({
            'status': 'success',
            'lang': lang,
            'entries': entries,
            'count': len(entries)
        })
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500


@app.route('/api/v1/ci/seo/v2/module/<state>')
def seo_v2_module(state):
    """Get module mapping and writes policy for a state"""
    try:
        from app.config.seo import seo_service
        if state not in seo_service.get_states():
            return jsonify({
                'status': 'error',
                'message': f'Invalid state: {state}'
            }), 400
        
        module = seo_service.get_module(state)
        writes_policy = seo_service.get_writes_policy(module)
        
        return jsonify({
            'status': 'success',
            'state': state,
            'module': module,
            'writes_policy': writes_policy
        })
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500


@app.route('/api/v1/ci/seo/v2/sitemap')
def seo_v2_sitemap():
    """Generate comprehensive sitemap with hreflang alternates"""
    try:
        from app.config.seo import seo_service
        base_url = request.args.get('base_url', '')
        entries = seo_service.generate_sitemap_entries(base_url)
        return jsonify({
            'status': 'success',
            'sitemap': entries,
            'count': len(entries)
        })
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500


# ===== New SEO Matrix API (Family Memory & Planning Hub) =====

@app.route('/api/v1/seo/matrix/strategy')
def seo_matrix_strategy():
    """Get product strategy and positioning"""
    try:
        from app.config.seo import get_seo_matrix_service
        service = get_seo_matrix_service()
        return jsonify({
            'status': 'success',
            'strategy': {
                'wedge_market': service.wedge_market,
                'core_promise': service.core_promise,
                'primary_cta': service.primary_cta,
                'non_goals': service.product_strategy.get('non_goals_now', [])
            }
        })
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500


@app.route('/api/v1/seo/matrix/modules')
def seo_matrix_modules():
    """Get all modules"""
    try:
        from app.config.seo import get_seo_matrix_service
        service = get_seo_matrix_service()
        return jsonify({
            'status': 'success',
            'modules': service.get_modules()
        })
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500


@app.route('/api/v1/seo/matrix/modules/<module_id>')
def seo_matrix_module(module_id):
    """Get specific module details"""
    try:
        from app.config.seo import get_seo_matrix_service
        service = get_seo_matrix_service()
        module = service.get_module(module_id)
        if not module:
            return jsonify({
                'status': 'error',
                'message': f'Module not found: {module_id}'
            }), 404
        return jsonify({
            'status': 'success',
            'module': module
        })
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500


@app.route('/api/v1/seo/matrix/categories')
def seo_matrix_categories():
    """Get all traffic categories"""
    try:
        from app.config.seo import get_seo_matrix_service
        service = get_seo_matrix_service()
        return jsonify({
            'status': 'success',
            'categories': service.get_traffic_categories()
        })
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500


@app.route('/api/v1/seo/matrix/patterns')
def seo_matrix_patterns():
    """Get all patterns (7×7 matrix)"""
    try:
        from app.config.seo import get_seo_matrix_service
        service = get_seo_matrix_service()
        module_id = request.args.get('module')
        patterns = service.get_all_patterns(module_id)
        return jsonify({
            'status': 'success',
            'patterns': patterns
        })
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500


@app.route('/api/v1/seo/matrix/patterns/<module_id>/<category_id>')
def seo_matrix_pattern(module_id, category_id):
    """Get specific pattern"""
    try:
        from app.config.seo import get_seo_matrix_service
        service = get_seo_matrix_service()
        pattern = service.get_pattern(module_id, category_id)
        if not pattern:
            return jsonify({
                'status': 'error',
                'message': f'Pattern not found: {module_id}/{category_id}'
            }), 404
        return jsonify({
            'status': 'success',
            'module': module_id,
            'category': category_id,
            'pattern': pattern
        })
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500


@app.route('/api/v1/seo/matrix/pages')
def seo_matrix_pages():
    """Get all pages"""
    try:
        from app.config.seo import get_seo_matrix_service
        service = get_seo_matrix_service()
        module_id = request.args.get('module')
        pages = service.get_all_pages(module_id)
        return jsonify({
            'status': 'success',
            'pages': pages,
            'count': len(pages)
        })
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500


@app.route('/api/v1/seo/matrix/sitemap')
def seo_matrix_sitemap():
    """Generate sitemap for all pages"""
    try:
        from app.config.seo import get_seo_matrix_service
        service = get_seo_matrix_service()
        base_url = request.args.get('base_url', 'https://cimeika.com')
        entries = service.generate_sitemap_entries(base_url)
        return jsonify({
            'status': 'success',
            'sitemap': entries,
            'count': len(entries)
        })
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500


@app.route('/api/v1/seo/matrix/sitemap.xml')
def seo_matrix_sitemap_xml():
    """Generate sitemap XML"""
    try:
        from app.config.seo import get_seo_matrix_service
        from flask import Response
        service = get_seo_matrix_service()
        base_url = request.args.get('base_url', 'https://cimeika.com')
        xml = service.generate_sitemap_xml(base_url)
        return Response(xml, mimetype='application/xml')
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500


@app.route('/api/v1/seo/matrix/robots.txt')
def seo_matrix_robots():
    """Generate robots.txt"""
    try:
        from app.config.seo import get_seo_matrix_service
        from flask import Response
        service = get_seo_matrix_service()
        sitemap_url = request.args.get('sitemap_url', 'https://cimeika.com/sitemap.xml')
        txt = service.generate_robots_txt(sitemap_url)
        return Response(txt, mimetype='text/plain')
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500


@app.route('/api/v1/seo/matrix/status')
def seo_matrix_status():
    """Get implementation status and execution strategy"""
    try:
        from app.config.seo import get_seo_matrix_service
        service = get_seo_matrix_service()
        return jsonify({
            'status': 'success',
            'implementation_status': service.status,
            'priority_order': service.get_priority_order(),
            'gates': service.get_gates()
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
