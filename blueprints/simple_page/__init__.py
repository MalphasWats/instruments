from flask import Blueprint, render_template

blueprint = Blueprint('simple_page', __name__,
                        template_folder='templates')
                        
                        
LABEL = 'Simple Page'
ADMIN_LABEL = 'Simple Page Administration'
ICON = 'globe'

import simple_page.core

def get_admin_panel():
    return render_template('widgets/admin_panel.html')