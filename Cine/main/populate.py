from models import Genre, User, Film, Rating
from datetime import datetime
from django.db.transaction import commit_on_success

path = "Cine\\csv"
    
@commit_on_success
def populateGenres():
    print("Loading Movie Genres...")
    
    fileobj = open(path + "\\genres.csv", "r")
    line = fileobj.readline()
    while line:  # Cada linea es un genero
        gen = line.split('\n')[0].strip().decode('utf-8', 'replace')
        Genre.objects.create(genreName=gen)
        line = fileobj.readline()
    fileobj.close()
    
    print("Genres inserted: " + str(Genre.objects.count()))
    print("---------------------------------------------------------")


@commit_on_success
def populateUsers():
    print("Loading users...")
    
    fileobj = open(path + "\\users.csv", "r")
    line = fileobj.readline()
    while line:
        data = line.split(',')
        if len(data) > 1:
            ide = data[0].strip()
            nam = data[1].strip()
            usuario = User.objects.filter(idUser=ide)
            if usuario:
                pass
            else:
                User.objects.create(idUser=ide,name=nam)   
        line = fileobj.readline()
    fileobj.close()
    
    print("Users inserted: " + str(User.objects.count()))
    print("---------------------------------------------------------")

@commit_on_success
def populateFilms():
    print("Loading movies...")
    
    fileobj = open(path + "\\films.csv", "r")
    line = fileobj.readline()
    while line:
        data = line.split('|')
        if len(data) > 1:
            ide = int(data[0].strip())
            tit = data[1].strip().decode('utf-8', 'replace')
            dir = data[2].strip().decode('utf-8', 'replace')
            rep = data[3].strip().decode('utf-8', 'replace')
            sin = data[4].strip().decode('utf-8', 'replace')
            date_rel = data[5].strip().decode('utf-8')
            enlace = data[6].strip().decode('utf-8', 'replace')
            med = None
            if data[7].strip():
                med= float(data[7].strip().replace(',','.'))
                usu = None
            if data[8].strip():
                usu= float(data[8].strip().replace(',','.'))
            sen = None
            if data[9].strip():
                sen= float(data[9].strip().replace(',','.'))
            list_genres = []
            if data[10].strip() != None:
                generos=data[10].split(',')
                for g in generos:
                    list_genres.append(g.strip())
            film = Film.objects.create(idMovie= ide,movieTitle=tit, director=dir, reparto=rep, synopsis=sin, releaseDate=date_rel,url=enlace, valor_medios=med, valor_usuarios=usu,
                                valor_sensacine=sen) 
            for c in list_genres:
                film.genres.add(Genre.objects.get(genreName=c))
                
        line = fileobj.readline()
    fileobj.close()
    
    print("Movies inserted: " + str(Film.objects.count()))
    print("---------------------------------------------------------")

       
@commit_on_success
def populateRatings():
    print("Loading ratings...")

    fileobj = open(path + "\\ratings.csv", "r")  # rb
    line = fileobj.readline()
    i = 0
    while line:
        data = line.split('|')
        if len(data) > 1:
            use = User.objects.get(idUser=data[0].strip())
            print data[1].strip()
            fil = Film.objects.get(idMovie=int(data[1].strip()))
            fecha = data[2].strip().split('/')
            dat = datetime(int(fecha[2]), int(fecha[1]), int(fecha[0]))
            if data[3].strip():
                rat= float(data[3].strip().replace(',','.'))
            Rating.objects.create(user=use, film=fil, rateDate=dat, rating=rat)
            i = i + 1
            if i % 10000 == 0:
                print(str(i) + " ratings have been saved...")
        line = fileobj.readline()
    fileobj.close()
       
    print("Ratings inserted: " + str(Rating.objects.count()))
    print("---------------------------------------------------------")
    
    
def populateDatabase():
    Rating.objects.all().delete()
    Film.objects.all().delete()
    usuarios = User.objects.all()
    for u in usuarios:
        u.delete()
    Genre.objects.all().delete()
    populateGenres()
    populateUsers()
    populateFilms()
    populateRatings()
     
    print("Finished database population")
    
if __name__ == '__main__':
    populateDatabase()
    
