from flask import Blueprint, jsonify
from extensions import db
from models import Detento
from sqlalchemy import func

dashboard_bp = Blueprint('dashboard', __name__, url_prefix='/api') 

@dashboard_bp.route('/dashboard_stats', methods=['GET']) 
def get_dashboard_stats():
    
    total_detentos = db.session.query(func.count(Detento.id)).scalar()

  
    status_counts_raw = db.session.query(Detento.status, func.count(Detento.id)).group_by(Detento.status).all()
    detentos_status = {status: count for status, count in status_counts_raw}

   
    all_statuses = ['Preso', 'Foragido', 'Solto', 'Condicional'] 
    for s in all_statuses:
        detentos_status.setdefault(s, 0) 

   
    crime_counts = {}
    detentos = Detento.query.all() 

    for detento in detentos:
        if detento.crimes_cometidos:
            
            crimes_list = [c.strip() for c in detento.crimes_cometidos.split(',') if c.strip()]
            for crime in crimes_list:
                
                normalized_crime = crime.capitalize() 
                crime_counts[normalized_crime] = crime_counts.get(normalized_crime, 0) + 1

    
    periculosidade_counts_raw = db.session.query(Detento.periculosidade, func.count(Detento.id)).group_by(Detento.periculosidade).all()
    detentos_periculosidade = {periculosidade: count for periculosidade, count in periculosidade_counts_raw}
    
   
    detentos_periculosidade.setdefault('Alta', 0)



    return jsonify({
        'total_detentos': total_detentos,
        'detentos_status': detentos_status,
        'crimes_comuns': crime_counts,
        'detentos_periculosidade': detentos_periculosidade
    })

