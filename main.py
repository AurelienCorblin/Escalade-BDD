import db
from flask import Flask, render_template, request, redirect, url_for, session
from passlib.context import CryptContext
password_ctx = CryptContext(schemes=['bcrypt'])

app = Flask(__name__)
app.secret_key = b'19647a95dad87c11a4b33c83943a5cdf9247a1f60e56dc6c0014d0305106a376'


@app.route("/accueil")
def accueil():
    with db.connect() as conn:
        with conn.cursor() as cur:
            cur.execute("select * from top_5_sites")
            lst = cur.fetchall()
    return render_template("accueil.html", sites = lst)

@app.route("/form")
def form():
    return render_template("inscription.html")

@app.route("/register", methods = ["POST"])
def register():
    email = request.form.get("email")
    mdp = request.form.get("mdp")
    if not mdp or not email:
        return redirect(url_for("form"))
    hash_pw = password_ctx.hash(mdp)
    with db.connect() as conn:
        with conn.cursor() as cur:
            cur.execute("insert into adherents(email,mdp) values(%s,%s)", (email,hash_pw))
    return redirect(url_for("connec"))

@app.route("/connec")
def connec():
    return render_template("connexion.html")

@app.route("/connexion", methods = ["POST"])
def connexion():
    email = request.form.get("email")
    mdp = request.form.get("mdp")
    if not mdp or not email:
        return redirect(url_for("connec"))
    with db.connect() as conn:
        with conn.cursor() as cur:
            cur.execute("select mdp from adherents where email=%s",(email,))
            mdp2 = cur.fetchone()
    if mdp2 == None:
        return redirect(url_for("connec"))
    if password_ctx.verify(mdp, mdp2.mdp):
        session["id"] = email
        return redirect(url_for("accueil"))
    return redirect(url_for("connec"))

@app.route("/deco")
def deco():
    session.pop("id")
    return redirect(url_for("accueil"))

@app.route("/profil")
def profil():
    if 'id' not in session.keys():
        return redirect(url_for("connec"))
    with db.connect() as conn:
        with conn.cursor() as cur:
            cur.execute("select id_diff from difficulte")
            lst = cur.fetchall()
            cur.execute("select email,nom,prenom,diff_fr,id_diff from adherents join difficulte on niveau=id_diff where email = %s", (session['id'],))
            info = cur.fetchone()
    niv =[info.id_diff]+[el.id_diff for el in lst]
    return render_template("profil.html", niv = niv, info = info)

@app.route("/updateProf", methods = ['POST'])
def updateProf():
    prenom = request.form.get('prenom')
    nom = request.form.get('nom')
    niveau = request.form.get('niveau')
    with db.connect() as conn:
        with conn.cursor() as cur:
            if prenom:
                cur.execute("update adherents set prenom = %s where email=%s", (prenom,session['id']))
            if nom:
                cur.execute("update adherents set nom = %s where email=%s", (nom,session['id']))
            if niveau:
                cur.execute("update adherents set niveau=%s where email=%s", (niveau,session['id']))
    return redirect(url_for("profil"))

@app.route("/membres")
def membres():
    with db.connect() as conn:
        with conn.cursor() as cur:
            cur.execute("select email,nom,prenom from adherents where email <> %s", (session['id'],))
            lst = cur.fetchall()
    return render_template("membres.html", mlist = lst)

@app.route("/profile/<string:email>")
def profile(email):
    with db.connect() as conn:
        with conn.cursor() as cur:
            cur.execute("select id_voie,nom_voie from voie natural join escalade natural join cordee natural join appartient where id_ad = %s;", (email,))
            lstvoie = cur.fetchall()
            cur.execute("select nom,prenom,diff_fr from adherents join difficulte on niveau=id_diff where email = %s", (email,))
            infoperso = cur.fetchone()
    return render_template("profile.html", voie = lstvoie, perso = infoperso,email=email)

@app.route("/profcordee/<string:email>")
def profcordee(email):
    with db.connect() as conn:
        with conn.cursor() as cur:
            cur.execute("select nom_cordee,prenom,nom from appartient join adherents on email = %s where id_ad = %s;", (email,email))
            cordee = cur.fetchall()
    return render_template("profcordee.html", cordee=cordee)

@app.route("/cordee")
def cordee():
    if 'id' not in session.keys():
        return redirect(url_for("connec"))
    with db.connect() as conn:
        with conn.cursor() as cur:
            cur.execute("select nom_cordee from cordee except select nom_cordee from appartient where id_ad = %s",(session['id'],))
            lstcord = cur.fetchall()
    return render_template("cordee.html", lstcord=lstcord) 

@app.route("/rejoindre")
def rejoindre():
    rejoint = request.args['rejoint']
    if not rejoint:
        return redirect(url_for('cordee'))
    with db.connect() as conn:
        with conn.cursor() as cur:
            cur.execute("insert into appartient(id_ad, nom_cordee) values(%s,%s)",(session['id'],rejoint))
    return redirect(url_for('cordee'))

@app.route("/creer", methods = ['POST'])
def creer():
    creer = request.form.get('creer')
    with db.connect() as conn:
        with conn.cursor() as cur:
            if creer:
                cur.execute("insert into cordee(nom_cordee) values(%s)",(creer,))
                cur.execute("insert into appartient(id_ad, nom_cordee) values(%s,%s)",(session['id'],creer))
    return redirect(url_for('cordee'))

@app.route("/guide")
def guide():
    localite = [None]
    voie = [None]
    with db.connect() as conn:
        with conn.cursor() as cur:
            cur.execute("select distinct nom_voie from voie")
            voie += cur.fetchall()
            cur.execute("select distinct localite from sitesescalade")
            localite += cur.fetchall()
            cur.execute("select * from controle_guide")
            controle_guide = cur.fetchall()
    return render_template("guide.html", localite = localite, voie = voie, controle_guide = controle_guide)

@app.route("/res_search_guid")
def res_search_guid():
    localite = request.args["localite"]
    voie = request.args["voie"]
    if not voie and not localite:
        return redirect(url_for("guide"))
    with db.connect() as conn:
        with conn.cursor() as cur:
            if localite:
                cur.execute("select id_guide,nom,prenom from exerce natural join guides join adherents on id_guide = email where localite = %s",(localite,))
            if voie:
                cur.execute("select id_guide,nom,prenom from sitesescalade natural join voie natural join exerce natural join guides join adherents on id_guide = email where diff <= niv_max and nom_voie = %s",(voie,))
            lst_guid = cur.fetchall()
    return render_template("res_guide.html", guid = lst_guid, voie = voie, localite = localite)

@app.route("/site")
def site():
    type = [None]
    localite = [None]
    site = [None]
    with db.connect() as conn:
        with conn.cursor() as cur:
            cur.execute("select distinct type_voie from voie")
            type+=cur.fetchall()
            cur.execute("select distinct localite from sitesescalade")
            localite+=cur.fetchall()
            cur.execute("select distinct nom_site from voie")
            site+=cur.fetchall()
    return render_template("site.html",type=type,localite=localite,site=site)




@app.route("/res_voie")
def res_voie():
    type = request.args['type']
    localite = request.args['localite']
    site = request.args['site']
    min_diff = request.args['min_diff']
    max_diff = request.args['max_diff']
    min_len = request.args['min_len']
    max_len = request.args['max_len']
    tmp = []
    with db.connect() as conn:
        with conn.cursor() as cur:
            cur.execute("select id_voie,nom_voie from voie order by nom_voie asc")
            lst_all = cur.fetchall()
            if type:
                cur.execute("select id_voie,nom_voie,type_voie,localite,nom_site,diff,longueur from voie natural join sitesescalade where type_voie = %s",(type,))
                tmp.append(cur.fetchall())
            if localite:
                cur.execute("select id_voie,nom_voie,type_voie,localite,nom_site,diff,longueur from voie natural join sitesescalade where localite = %s",(localite,))
                tmp.append(cur.fetchall())
            if site:
                cur.execute("select id_voie,nom_voie,type_voie,localite,nom_site,diff,longueur from voie natural join sitesescalade where nom_site = %s",(site,))
                tmp.append(cur.fetchall())
            if min_diff and max_diff:
                cur.execute("select id_voie,nom_voie,type_voie,localite,nom_site,diff,longueur from voie natural join sitesescalade where diff > %s and diff < %s",(min_diff,max_diff))
                tmp.append(cur.fetchall())
            elif min_diff:
                cur.execute("select id_voie,nom_voie,type_voie,localite,nom_site,diff,longueur from voie natural join sitesescalade where diff > %s",(min_diff,))
                tmp.append(cur.fetchall())
            elif max_diff:
                cur.execute("select id_voie,nom_voie,type_voie,localite,nom_site,diff,longueur from voie natural join sitesescalade where diff < %s",(max_diff,))
                tmp.append(cur.fetchall())
            if min_len and max_len:
                cur.execute("select id_voie,nom_voie,type_voie,localite,nom_site,diff,longueur from voie natural join sitesescalade where longueur < %s and longueur > %s",(max_len,min_len))
                tmp.append(cur.fetchall())
            elif min_len:
                cur.execute("select id_voie,nom_voie,type_voie,localite,nom_site,diff,longueur from voie natural join sitesescalade where longueur > %s",(min_len,))
                tmp.append(cur.fetchall())
            elif max_len:
                cur.execute("select id_voie,nom_voie,type_voie,localite,nom_site,diff,longueur from voie natural join sitesescalade where longueur < %s",(max_len,))
                tmp.append(cur.fetchall())
    lst1 = []
    for elem in tmp:
        for v in elem:
            if v not in lst1:
                lst1.append(v)
    lst2 = []
    for elem in lst1:
        if min_len and str(elem.longueur) <= min_len: 
            lst2.append(elem)
            continue
        if max_len and str(elem.longueur) >= max_len:
            lst2.append(elem)
            continue
        if min_diff and str(elem.diff) <= min_diff: 
            lst2.append(elem)
            continue
        if max_diff and str(elem.diff) >= max_diff:
            lst2.append(elem)
            continue
        if site and elem.nom_site != site:
            lst2.append(elem)
            continue 
        if localite and elem.localite != localite:
            lst2.append(elem)
            continue 
        if type and elem.type_voie != type:
            lst2.append(elem)
            continue
    lst = []
    for elem in lst1:
        if elem not in lst2:
            lst.append(elem)
    return render_template("res_voie.html", lst_all = lst_all,lst=lst)
            



@app.route("/prof_voie/<int:id>")
def prof_voie(id):
    d = []
    with db.connect() as conn:
        with conn.cursor() as cur:
            cur.execute("select nom_voie,localite,diff_fr,type_voie,longueur,nom_site from voie natural join sitesescalade join difficulte on diff=id_diff where id_voie = %s",(id,))
            info = cur.fetchall()
            cur.execute("select distinct nom_type from typesescalade")
            type = [elem.nom_type for elem in cur.fetchall()]
            for elem in type:
                cur.execute("select distinct nom_type,esc_date,nom_cordee from voie natural join sitesescalade natural join escalade where id_voie = %s and nom_type = %s order by esc_date limit 1",(id,elem))
                tmp = cur.fetchall()
                if tmp:
                    d.append(tmp)
    return render_template("prof_voie.html", info=info, d=d)

@app.route("/sortie")
def sortie():
    if 'id' not in session.keys():
        return redirect(url_for("connec"))
    with db.connect() as conn:
        with conn.cursor() as cur:
            cur.execute("select * from sorties natural left join (select id_sortie,count(id_ad) as nbpart from participe group by id_sortie)as \
            nb where niv_min <= (select niveau from adherents where email = %s) and createur <> %s and max_part > nbpart and date_sortie > now() except select \
            distinct sorties.id_sortie,sortie_desc,date_sortie,niv_min,site_sortie,max_part,createur,nbpart from sorties natural left join \
            (select id_sortie,count(id_ad) as nbpart from participe group by id_sortie)as nb,participe \
            where participe.id_sortie=sorties.id_sortie and id_ad = %s",(session['id'],session['id'],session['id']))
            affiche = cur.fetchall()
            cur.execute("select * from sorties natural left join (select id_sortie,count(id_ad) as nbpart from participe group by id_sortie)as \
            nb where createur = %s and date_sortie > now()",(session['id'],))
            messorties = cur.fetchall()
            cur.execute("select * from cordee")
            cord = [elem.nom_cordee for elem in cur.fetchall()]
            i=0
            while i < len(messorties):
                test = "cordee sortie n°"+str(messorties[i].id_sortie)
                if test in cord:
                    messorties.pop(i)
                else:
                    i+=1
            cur.execute("select distinct sorties.id_sortie,sortie_desc,date_sortie,niv_min,site_sortie,max_part,createur,nbpart \
            from sorties natural join (select id_sortie,count(id_ad) as nbpart from participe group by id_sortie)as nb,participe \
            where participe.id_sortie=sorties.id_sortie and id_ad = %s and date_sortie > now()",(session['id'],))
            participe=cur.fetchall()
            cur.execute("select id_diff from difficulte")
            diff = cur.fetchall()
            cur.execute("select nom_site from sitesescalade")
            site = cur.fetchall()
    return render_template("sortie.html", diff=diff, affiche=affiche, messorties=messorties, participe=participe, site=site)

@app.route("/participe")
def participe():
    participe = request.args['participe']
    with db.connect() as conn:
        with conn.cursor() as cur:
            cur.execute("insert into participe(id_ad,id_sortie) values(%s,%s)",(session['id'],participe))
    return redirect(url_for('sortie'))

@app.route("/creersortie", methods = ['POST'])
def creersortie():
    desc = request.form.get('desc')
    date = request.form.get('date')
    site = request.form.get('site')
    max_part = request.form.get('maxpart')
    niv_min = request.form.get('niv_min')
    if not desc or not date or not site or not max_part or not niv_min:
        return redirect(url_for('sortie'))
    with db.connect() as conn:
        with conn.cursor() as cur:
            cur.execute("insert into sorties(sortie_desc,date_sortie,niv_min,site_sortie,max_part,createur) values(%s,%s,%s,%s,%s,%s)",(desc,date,niv_min,site,max_part,session['id']))
            cur.execute("select id_sortie from sorties where sortie_desc = %s and date_sortie = %s and niv_min = %s and site_sortie = %s and\
                max_part = %s and createur = %s",(desc,date,niv_min,site,max_part,session['id']))
            id = cur.fetchone()
            cur.execute("insert into participe(id_ad,id_sortie) values(%s,%s)",(session['id'],id))
    return redirect(url_for('sortie'))

@app.route("/gest_sortie", methods = ['POST'])
def gest_sortie():
    annuler = request.form.get('annuler')
    valider = request.form.get('valider')
    with db.connect() as conn:
        with conn.cursor() as cur:
            if(annuler):
                cur.execute("DELETE FROM participe WHERE id_sortie = %s",(annuler,))
                cur.execute("DELETE FROM sorties WHERE id_sortie = %s",(annuler,))
            if valider and not annuler :
                nom_cord = "cordee sortie n°"+str(valider)
                cur.execute("select id_ad from participe where id_sortie = %s",(valider,))
                lst_ad = cur.fetchall()
                cur.execute("insert into cordee(nom_cordee) values(%s)",(nom_cord,))
                for elem in lst_ad:
                    cur.execute("insert into appartient(id_ad,nom_cordee) values(%s,%s)",(elem,nom_cord))
    return redirect(url_for('sortie'))

@app.route("/devientguide")
def devientguide():
    if 'id' not in session.keys():
        return redirect(url_for("connec"))
    with db.connect() as conn:
        with conn.cursor() as cur:
            cur.execute("select id_guide from guides where id_guide = %s", (session['id'],))
            guide = cur.fetchone()
            cur.execute("select id_diff from difficulte,adherents where email = %s and id_diff <= niveau",(session['id'],))
            diff = cur.fetchall()
            cur.execute("select distinct localite from sitesescalade except select localite from exerce where id_guide = %s",(session['id'],))
            localite = cur.fetchall()
            cur.execute("select localite from exerce where id_guide = %s",(session['id'],))
            exerce = cur.fetchall()
    return render_template("devientguide.html",exerce=exerce,guide=guide,diff=diff,localite=localite)

@app.route("/creerguide",methods = ['POST'])
def creerguide():
    niv_max = request.form.get('niv_max')
    with db.connect() as conn:
        with conn.cursor() as cur:
            cur.execute("insert into guides(id_guide,niv_max) values(%s,%s)",(session['id'],niv_max))
    return redirect(url_for('devientguide'))

@app.route("/exerceguide",methods = ['POST'])
def exerceguide():
    localite = request.form.get('localite')
    with db.connect() as conn:
        with conn.cursor() as cur:
            cur.execute("insert into exerce(id_guide,localite) values(%s,%s)",(session['id'], localite))
    return redirect(url_for('devientguide'))


if __name__ == '__main__':
    app.run()