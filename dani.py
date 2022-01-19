from flask import Flask, request
import datetime, random
import requests
from twilio.twiml.messaging_response import MessagingResponse

app = Flask(__name__)

curr_min = -1
curr_maj = 0
curr_month = 0
curr_hp = 9
curr_mental = 9
max_hp = 9
max_mental = 9
curr_event = -1

month0 = {'month':'Mar 2019', 'events':[
    {'desc':'Llegas a Polanco, donde vas a empezar un nuevo trabajo. Llegas el mismo día que un futuro roomie quien te ve feo. Para tu sorpresa, él te regala una bolsa para super cuando se te olvidó una y te prepara hot cakes para tu primer día laboral.', 'effects':[999,999], 'num_min': 1},
    {'desc':'Tus Roomies te invitan a ir a Big Red! Tomas un poco pero te reanima!', 'effects':[-1,1], 'num_min': 1},
    {'desc':'Sales a tomar al Bar de Polanquito con tus compañeros de trabajo. Tomas demasiado y ni sabes cómo llegas a tu cuarto.', 'effects':[-3,-3], 'num_min': 1}
]}

month1 = {
    'month':'Abr 2019', 'events':[
        {'desc':'Dejan plantado a tu roomie :c Lo invitas a comer tapas y te la pasas increíble con él! aún estás un poco enojada que lo plantaron D:< y por eso pierdes 2 salud', 'effects':[-2,2], 'num_min': 1},
        {'desc':'Vas a una fiesta en la que te piden que te metas a la cama con quien te invitó. Esa Claudia es una loquilla! xD', 'effects':[-2,-2], 'num_min': 1},
        {'desc':'Tu roomie te deja un libro para tu viaje. No lo lees completo, pero te gusta el gesto.', 'effects':[0,2], 'num_min': 1},
        {'desc':'Te invitan a una fiesta con los mejores tacos al pastor que has probado! gana 1 punto de vida máxima', 'effects':[999,0], 'num_min': 1}
    ]
}

month2 = {
    'month':'May 2019', 'events':[
        {'desc':'Sales con tu roomie a escuchar Jazz en vivo. Llegas a un lugar que se llama Zinco en un "sótano de iglesia." Aún así, te la pasas increíble (Aunque tu roomie se ve que ya le afectó su jack daniels honey).', 'effects':[0,1], 'num_min': 1},
        {'desc':'Encuentras a tu roomie haciendo huevito con salchicha en calzones. Yuck', 'effects':[-1,-1], 'num_min': 1},
        {'desc':'A tu roomie se le cae su pan con ajo mientras estás de viaje. Su tristeza infinita se te contagia un poco :c', 'effects':[1,-2], 'num_min': 1},
        {'desc':'Preparas un evento increíble para Ikea! Todos te elogian en demasía! Eres tan feliz que recibes 1 punto de salúd mental máxima!', 'effects':[1,999], 'num_min': 1},
    ]
}

month3 = {
    'month':'Jun 2019', 'events':[
        {'desc':'Viajas a Estados Unidos. La comida falsa en el aeropuerto te desespera, y te cansas demasiado, dañando tu salúd mental y tu salúd física.', 'effects':[-2,-2], 'num_min': 1},
        {'desc':'Tienes una reunión con Carlos, Marco y Edgar! Te sorprendes que Muciño según "No ha hecho nada" y no hay nada que no haya hecho O.O', 'effects':[0,-1], 'num_min': 1},
        {'desc':'Vas a McCarthy\'s con tu roomie. Lo invitas a tomar una botella de vino. Él te dice que hay que tomarla en el baño 🤦‍♂️. Le escribes una nota y le dedicas la canción "always in my head." Te la pasas tan bien que ganas 1 punto de vida máxima y de salúd mental!', 'effects':[999,999], 'num_min': 1},
        {'desc':'Tu roomie te dice que no hay que refrigerar las salsas. Tú le dices que sí y que "esto es muy de novia pero no me vas a cambiar". Él le pregunta a una experta y lo regaña porque le dice que sí hay que refrigerar. Te ayuda a tu salúd mental!', 'effects':[0,2], 'num_min': 1},
    ]
}

month4 = {
    'month':'Jul 2019', 'events':[
        {'desc':'Muere la mejor amiga de tu roomie. Él llora en tus brazos y te agradece todo lo que has hecho por él.', 'effects':[0,-2], 'num_min': 2},
        {'desc':'Se te olvida el candado de tu maleta. Oops!', 'effects':[0,-2], 'num_min': 2}
    ]
}
month5 = {
    'month':'Ago 2019', 'events':[
        {'desc':'Tu roomie y tú pierden un sábado entero buscando una piña. Cuando la encuentran, no preparas la piña asada que se te antojaba. <PD: Me debes una piña asada!>', 'effects':[0,5], 'num_min': 1},
        {'desc':'Descubres que tu roomie hace cappuccinos buenísimos y brownies... pasables. Pero de regreso en uno de tus viajes, hace un brownie que amaste!', 'effects':[3,3], 'num_min': 1}
    ]
}
month6 = {
    'month':'Sept 2019', 'events':[
        {'desc':'Se te pierden las maletas en un viaje laboral. Te enfermas feo :c', 'effects':[-3,-3], 'num_min': 2},
        {'desc':'Haces un viaje a Florida en el que encaras tener que comer el tocino. NO QUIERES COMER EL TOCINO, AAAAAAAAAAAAAH', 'effects':[-2,-2], 'num_min': 1},
    ]
}
month7 = {
    'month':'Oct 2019', 'events':[
        {'desc':'Llega una nueva roomie que ocupa todo el refri y lo deja fatal. ESOS SON HONGOS!?!?!??', 'effects':[-1,-3], 'num_min': 3}
    ]
}
month8 = {
    'month':'Nov 2019', 'events':[
        {'desc':'Tu Roomie descubre que te encantan las Hojaldres/Panes de Muertos. Se espanta que le dices Hojaldres. Te invita un monton de Hojaldres. <Me gusta decir Hojaldre :B>', 'effects':[1,1], 'num_min': 2},
        {'desc':'Tienes una visita de corporativo de Ikea! Todos quedan impresionados contigo! Gana 1 punto de vida y de salud mental máximos!', 'effects':[999,999], 'num_min': 1}
    ]
}
month9 = {
    'month':'Dic 2019', 'events':[
        {'desc':'Le festejas el cumpleaños de tu roomie con vino y con legos. Le encanta, y promete siempre mantenerlos cerca. <Se rumora que aún los guarda al lado de su cama 🥺 >', 'effects':[3,3], 'num_min': 2},
        {'desc':'Vas a Six Flags con tu roomie. Es uno de los mejores y más memorables días que has tenido. Gana 1 punto de vida y de salúd mental máximos!', 'effects':[999,999], 'num_min': 1},
        {'desc':'Tu roomie y tú compran San Ginés después de tanto tiempo sin que los comas! Te hacen feliz esos churros <3', 'effects':[0,3], 'num_min': 1},
        {'desc':'Vas a una boda de tus amigos en Puebla, y te la pasas increíble en ella!', 'effects':[1,1], 'num_min': 2},
    ]
}
month10 = {
    'month':'Ene 2020', 'events':[
        {'desc':'Te resignas a que vas a tener que comer el tocino. Te hace sentir mal esto.', 'effects':[-1,-3], 'num_min': 2},
        {'desc':'Retomas correr, lo cual te hace muy feliz. Gana un punto de vida máxima!', 'effects':[999,3], 'num_min': 2},
        {'desc':'Tu roomie te compra audífonos Sony para tus viajes!', 'effects':[1,3], 'num_min': 1},
    ]
}
month11 = {
    'month':'Feb 2020', 'events':[
        {'desc':'Corres una carrera de 10k que no pensabas que podrías correr! Todos están muy orgullosos de ti! <Sigo MUY orgulloso que hayas corrido tanto.> Gana un punto de vida máxima y salúd mental máxima!', 'effects':[999,999], 'num_min': 2},
        {'desc':'Cortan la Luz en Plinio. Pierdes un buen de comida y eso te hace triste :c', 'effects':[0,-1], 'num_min': 1},
        {'desc':'Tu roomie te invita a nadar con él! Nunca pensaste que algo tan tonto como otro nadador en el carril le dieran celos 🤦‍♂️', 'effects':[1,1], 'num_min': 1},
        {'desc':'Conoces el centro de Guadalajara con las Niñas de la empresa! Cómo te tratan te hace muy feliz C:', 'effects':[0,1], 'num_min': 1},
    ]
}
month12 = {
    'month':'Mar 2020', 'events':[
        {'desc':'Tu roomie te compra una vela de flor que toca canciones y gira. Te encanta!', 'effects':[1,3], 'num_min': 2},
        {'desc':'Empieza la pandemia! No sabes lo complicadas que se van a poner las cosas, pero todos te apoyan y están orgullosos de lo que haces', 'effects':[-1,-1], 'num_min': 2}
    ]
}

maj_events = [month0,month1,month2,month3,month4,month5,month6,month7,month8,month9,month10,month11,month12]

min_events = [
    {"desc":'Vas tarde al trabajo, pero se te antoja muchísimo bañarte con agua caliente!',
    "opts" : ["Jugartela y bañarte con agua calientita","Bañarte rápido con agua fría :c"],
    "effects" : [[-1,1],[1,-1]]},
    {"desc":'Es tarde y se te antoja un aperitivo.',
    "opts" : ["Tomarte un pan con jamón serrano.","Esperar a la cena saludable :c", "Ir por un pan!"],
    "effects" : [[0,1],[1,1],[1,1]]},
    {"desc":'Tu roomie trajo compañía. No puedes concentrarte en trabajar >:C',
    "opts" : ["Intentar acabar el trabajo","Irte a dormir y tratar de ignorarlos", "Salir a ver si se cansan en la tarde"],
    "effects" : [[0,-1],[-1,-1],[1,1]]},
    {"desc":'Es viernes y tienes ganas de hacer algo!',
    "opts" : ["Salir con amigos","Salir a caminar", "Leer algo!", "Mandarle mensaje a Edgar a ver si McCarthy's está abierto"],
    "effects" : [[2,2],[3,0],[0,3],[3,3]]},
    {"desc":'Se te olvidó ir al super!',
    "opts" : ["Pedir comida","No comer nada", "Comer el plátano arrinconado que está ahí."],
    "effects" : [[2,2],[-2,-2],[-2,2]]},
    {"desc":'Estás en el trabajo y tienes un bloqueo mental.',
    "opts" : ["Decidir regresar a Plinio","Dar una vuelta para despejar la mente"],
    "effects" : [[1,1],[1,1]]},
    {"desc":'Se te antojan unas trufas de chocolate. Las compras y...',
    "opts" : ["Compartirlas con Edgar","Comérmelas todaaaaaaaas"],
    "effects" : [[1,1],[3,0]]},
    {"desc":'Está siendo un día perfecto afuera para caminar!',
    "opts" : ["Ir a caminar!","Trabajar"],
    "effects" : [[1,0],[0,1]]},
    {"desc":'Te sientes sola.',
    "opts" : ["Le hablas a tu mamá","Le hablas a un amigo", "Le mandas un mensaje a Edgar"],
    "effects" : [[1,3],[2,2],[3,1]]},
    {"desc":'Tienes sed de la mala',
    "opts" : ["Te esperas a que se arme plan","Le mandas mensaje a Edgar a ver qué hay", "Tomas por ti misma"],
    "effects" : [[1,-1],[1,1],[2,-1]]},
    {"desc":'Tu hermano te manda algo muy gracioso',
    "opts" : ["Reirte","Hablar horas con él"],
    "effects" : [[1,1],[0,3]]},
    {"desc":'Te sientes enferma',
    "opts" : ["Decirle a Edgar que te acompañe","Ir sola al Dr Simi"],
    "effects" : [[-1,0],[-1,0]]},
    {"desc":'Quieres disfrutar de que estas sola en el depto',
    "opts" : ["Pones música de la buena","Realizar 'el deporte'"],
    "effects" : [[2,2],[3,3]]},
    {"desc":'Te sientes anonadada por el futuro',
    "opts" : ["Ponerte a pensar sobre todo lo bueno que te ha pasado","Llorar"],
    "effects" : [[1,0],[-1,1]]},
    {"desc":'Extrañas los buenos días en el Tec',
    "opts" : ["Mandarle mensaje a una amiga","Hacer planes para visitar al tec"],
    "effects" : [[0,1],[0,1]]},
    {"desc":'Te sientes con mucha energía y muy feliz',
    "opts" : ["Bailar","Correr"],
    "effects" : [[2,2],[4,0]]},

]

@app.route('/wabot', methods=['POST'])
def wabot():
    global curr_min
    global curr_event
    global curr_maj
    global curr_month
    global curr_hp
    global curr_mental
    global max_hp
    global max_mental
    global maj_events
    global min_events

# curr_min = -1
# curr_maj = 0
# curr_month = -1
# curr_hp = 9
# curr_mental = 9
# max_hp = 9
# max_mental = 9

    content = request.values.get('Body', '').lower()

    if 'trampa' in content.lower():
        curr_hp = 99
        curr_mental = 99
        max_hp = 99
        max_mental = 99

    if 'reset' in content.lower():
        curr_min = -1
        curr_maj = 0
        curr_month = -1
        curr_hp = 9
        curr_mental = 9
        max_hp = 9
        max_mental = 9

    if curr_event != -1:
        for i in range(0,len(min_events[curr_event]['effects'])):
            if str(i+1) in content:
                curr_hp += min_events[curr_event]['effects'][i][0]
                curr_mental += min_events[curr_event]['effects'][i][1]
                if curr_hp > max_hp:
                    curr_hp == max_hp
                if curr_mental > max_mental:
                    curr_mental == max_mental
                
    
    if curr_min == -1:
        if curr_maj == len(maj_events[curr_month]['events']) - 1:
            curr_month += 1
            if curr_month == len(maj_events):
                        resp = MessagingResponse()
                        msg = resp.message()
                        msg.body(f"Acabaste mi juego! Felicidades! Ojalá te haya gustado :)")
                        curr_min = -1
                        curr_maj = 0
                        curr_month = -1
                        curr_hp = 9
                        curr_mental = 9
                        max_hp = 9
                        max_mental = 9
    
            curr_maj = 0
        curr_hp += maj_events[curr_month]['events'][curr_maj]['effects'][0]
        curr_mental += maj_events[curr_month]['events'][curr_maj]['effects'][1]
        if(maj_events[curr_month]['events'][curr_maj]['effects'][0] == 999):
            max_hp += 1
            curr_hp = max_hp
        if(maj_events[curr_month]['events'][curr_maj]['effects'][1] == 999):
            max_mental += 1
            curr_mental = max_mental

        if curr_hp > max_hp:
            curr_hp == max_hp
        if curr_mental > max_mental:
            curr_mental == max_mental
        
        curr_min = 0
        curr_event = -1
        resp = MessagingResponse()
        msg = resp.message()
        msg.body(f"Es {maj_events[curr_month]['month']}.\n"+maj_events[curr_month]['events'][curr_maj]['desc']+"\n"+f"Tienes {curr_hp}/{max_hp} de vida y {curr_mental}/{max_mental} de salud mental. Manda CONTINUAR para seguir jugando!")
    
    else:
        if curr_min + 1 == maj_events[curr_month]['events'][curr_maj]['num_min']:
            curr_min = -1
            curr_maj += 1
        else:
            curr_min += 1
        curr_event = random.randrange(0,len(min_events))
        Body = f"Es {maj_events[curr_month]['month']}.\n"
        Body += min_events[curr_event]['desc']+"\n"
        i = 1
        for opt in min_events[curr_event]['opts']:
            Body += f"Manda {i} si quieres {opt}.\n"
            i += 1
        Body += f"Tienes {curr_hp}/{max_hp} de vida y {curr_mental}/{max_mental} de salud mental."
        resp = MessagingResponse()
        msg = resp.message()
        msg.body(Body)
    
    print(str(resp))
    return str(resp)


if __name__ == "__main__":
    app.run(host='0.0.0.0',port=80)
