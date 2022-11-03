
def get_link_image(target, etape):
    if etape == 1:
        target_lnk_img = target.find('div', class_="item active").find('img')['src']
    elif etape == 2:
        target_lnk_img = target['image']
    elif etape == 3:
        target_lnk_img = target['src']
    else:
        return None
    base_url = "https://books.toscrape.com/"
    complete_lnk = base_url + target_lnk_img
    complete_lnk = complete_lnk
    return complete_lnk.replace("../../", '')

"""
#Rajouter un if qui va dire si dans l'étape une tu apelles
une seule fonction get link image avec deux parametre 
target = soup ou book get_link_image_horror
variable etape aurre parametre qui peut prendre 1 ou 2 en fonction de l'étape ou on va se trouver /

Get image un if si etape = 1 alors on va dire target link image = soup 
si etape = 2 alors on va dire target link = book horror[image] """
