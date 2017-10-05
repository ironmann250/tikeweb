from django import template                                                                                                              
from django.conf import settings 
import random                                                                                                        

register = template.Library()                                                                                                            
rand=random.WichmannHill()
production=True
#return nothing in production to enable caching 
#for a faster load
@register.simple_tag(name='cache_bust')                                                                                                  
def cache_bust():                                                                                                                        

    if not production:                                                                                                                   
        version = random.randint(100,10000)    
        return '__v__={version}'.format(version=version)
    else:                                                                                                                                
        return ''                                                                                                               

    
