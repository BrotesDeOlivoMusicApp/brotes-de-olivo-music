#!/usr/bin/env python3
import hashlib
import json
import sqlite3
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DB = ROOT / "data" / "brotes_publica.sqlite"
VERSION = ROOT / "data" / "version.json"

CHORDS = {
"C0011": """[Am]Mi hermano no puede mo[G]rir, mi hermano no puede morir.
[F]Mi hermano no puede morir, ¡no puede!, no puede mo[Am]rir,
[Dm]es mi hermano, ¡es mi her[Am]mano![E][Am]
[Am]Si está enfermo no puede mo[G]rir, tras rejas no puede morir,
[F]hambriento no puede morir, si es niño no puede mo[Am]rir,
[Dm]si es joven no puede morir, si anciano no puede mo[Am]rir,
[G]¡es mi her[Am]mano!
[Am]La tierra no puede mo[G]rir, el mundo no puede morir,
[F]el cosmos no puede morir, no puede, no puede mo[Am]rir,
[Dm]¡es mi hermano! ¡es mi her[Am]mano![E][Am]
[Am]Si es árbol no puede mo[G]rir, si es fiera no puede morir,
[F]si es roca no puede morir, si es cielo no puede mo[Am]rir,
[Dm]si es mar no puede morir, la vida no puede mo[Am]rir,
[G]¡es mi her[Am]mano!""",
"C0014": """[C]La vida de un misionero es dichosa cuando es [F]libre,
[C]no se ata a la tierra y de todo se des[G]pide.
[F]No echará raíz alguna, cual viajero incan[C]sable,
[G]sintiendo el total despojo, sin nada que a él le ate.
¤ [C]Un amor a reco[G]rrer, [C]la justicia [C7]como a[F]fán,[Dm7][G]
[C]con la fe en la provi[F]dencia, siendo [C]obreros de la [F]paz.[G]
[F]Con la humildad del pe[G]sebre [C]todo el orbe cubri[F]ré,[Dm7][G]
[C]porque a servir a los más [F]pobres [C]yo mi vida consa[F]gré.[C][G][C]
[C]No quedaré insensible ante el clamor de los [F]pueblos,
[C]he de hacer presente en mí la miseria que hay en [G]ellos.
[F]Un pesebre de comienzo y una cruz como fi[C]nal,
[G]es lo que Jesús vivió, y en él yo quiero alcanzar. ¤""",
"C0015": """[D]Espero un día que nunca oscurezca,
[G]noches suaves en [D]calma... [Em]¿cuándo se[A]rá?
[D]Aguardo un sol que abrase las almas,
[G]niños que no se en[D]tristezcan [G]ya nunca [A]más.
¤ [D]No pierdo la espe[G]ranza de un [D]sol abrasa[G]dor.[Em][A]
[D]El mundo un grito [G]lanza: [D]¿adónde fue el a[G]mor?[Em][A]
[D]Con ansia espero la primavera,
[G]que a mi alma dé [D]vida nueva... [Em]¿llega[A]rá?
[D]Ver madres que no se sientan cansadas,
[G]tras una dura jor[D]nada, [G]¡que sea [A]ya!
[D]¿Cuándo vendrá el ma[G]ñana que va[D]yamos hacia [G]Dios,[Em][A]
[D]con manos afer[G]radas, [D]alegres y con a[G]mor?[Em][A]
[D]Espero hombres de paz en la tierra,
[G]jamás naciones en [D]guerra... [Em]¿cuándo ven[A]drá?
[D]Los hombres teniendo todos trabajo,
[G]felices siempre [D]aquí abajo... [G]¡que sea [A]ya! ¤
[D]Espero verme con Dios en la calle,
[G]en esos hombres que [D]pasan [Em]en sole[A]dad.
[D]Aguardo poder sentir la alegría
[G]de ver nacer ese [D]día [G]en que tú ven[A]drás... ¤
[D]¿Cuándo vendrá el ma[G]ñana que va[D]yamos hacia [G]Dios,[Em][A]
[D]con manos afer[G]radas, [D]alegres y con a[G]mor?[Em][A]""",
"C0130": """[Am]Allanad, [A7]allanad los [Dm]caminos, que viene el [E]Señor.
[Am]Pasará, [A7]pasará por tu [Dm]lado sediento de [E7]amor.
[Am]Él ca[E]mina con [Am]vosotros, [E]no le [Am]cono[E7]céis[Am],
[E]te acompaña en tu [Am]camino, [E]vives tú [Am]con [E]él[Am].
[C]Es el pobre que se acerca buscando tu [G]comprensión,
[C]es el triste que deambula [G]sediento de [F]paz y [E7]amor.
[C]Tú has de ser quien pondrá la sonrisa en su [G]corazón,
sembrarás una flor en su campo falto de [C]Dios.
Caminad, caminad los senderos que marca el Señor.
Y quitad, y quitad las espinas de su corazón.
[Am]Él te [E]busca, [Am]él te [E]llama, [Am]quiere tu [E7]leal[Am]tad,
[E]entre rejas, en las [Am]guerras, [E]esperando [Am]está.
[C]Vive enfermo en las cabañas con [G]hambre de [F]luz y [E7]pan,
[C]es el rico de [G]dinero que [F]harto de todo [E7]está.
[C]Allanad y quitad los pedriscos que hay al [G]andar,
descansadle los pies al descalzo que andando [C]va.""",
"C0131": """[D]A una [A]boda [D]Cristo [A]fue y [D]María [A]iba con [D]él[A],
[D]a Ca[A]ná de [D]Gali[A]lea un [D]milagro [A]iba a [D]hacer[A].
[D]En las fiestas de la boda todo es [G]felici[D]dad,
[E]mas el vino que han traído pronto se va a aca[A]bar.
[D]María a Jesús se acercó. [A]“No [G]tienen vino, [D]¿qué vas a [E]hacer?”[A]
[D]“A ti y a mí qué, mujer. [A]No ha [G]llegado aún [D]mi que[E]hacer”[A].
[D]Mas la [A]madre dijo a [D]los [A]siervos: [D]“Haced lo [A]que os diga [D]él”[A].
[D]Jesús [A]dice a los [D]criados: [A]“Seis [D]tinajas [A]acá [D]traed[A].
[D]Echen agua en las tinajas, [G]dejándolas col[D]mar;
[E]pronto tendremos el vino y al maestre presen[A]tar”.
[D]Los criados llevan vino [G]hasta el vina[D]dor
[G]y el maestre, extrañado, al esposo [A]lla[D]mó.
[D]“Se estila en todo lugar [A]dar lo [G]bueno, [D]luego el [E]mal[A].
[D]Y en esta boda encontré [A]lo me[G]jor para el [D]final”[E][A].
[D]En Caná de Galilea un [G]milagro o[D]bró;
[E]fue el primero de los muchos que haría el Se[A]ñor.""",
"C0133": """[Dm]Al pozo de Jacob llegó un día el [C]Señor, su cara empapada en [F]sudor,
[C]sus labios resecos de [F]sed; [Dm]junto al [A7]brocal [Dm]descan[F]só[A7][Dm].
[Dm]Se acerca por el [C]camino una [F]samaritana y [C]al llegar al [F]pozo,
[A7]Jesús ex[Bb]clama: [A7]“[Dm]Dame agua [A7]buena mujer, [Dm]tengo [Gm]sed”[Dm].
[Dm]“No entiendo que siendo [C]judío te atrevas al [F]pozo a venir,
[C]tu pueblo es impuro, es [F]judío, [A7]no sé qué de[Dm]cir”.
[Dm]“Si supieras quién pide [C]agua, más bien tú le pedi[F]rías.
[A7]Yo podría [Bb]darte el agua [A7]viva: [Dm]con mi agua [A7]no tendrás mas [Dm]sed”[Gm][Dm].
[Dm]“De ese agua [A7]dame de beber: [Dm]tengo [Gm]sed, sed de [Dm]ti, tengo [A7]sed”[Dm][F][A7][Dm].""",
"C0135": """[E]¤ Tú eres, [B7]Señor, el [E]Pan de [A]Vi[E][B7][E],
[E]mi vida [B7]sin ti [E]no será [A]vi[E][B7][E]da.
[E]“El pan que yo os daré ha de [A]ser mi [B7]propia [E]carne”.
[E]Contigo viviré cuando [A]coma [B7]de tu [E]pan. ¤
[E]Aquel que cree en ti tiene ya [A]la vida [B7]eter[E]na.
[E]Si como de tu pan de tu [A]vida [B7]goza[E]ré. ¤
[E]“Mi Padre es quien os da verda[A]dero pan [B7]del [E]cielo
[E]y a la tierra bajó para el [A]mundo [B7]alimen[E]tar”. ¤
[E]Quien come de tu pan no pade[A]cerá más [B7]ham[E]bre.
[E]Quien bebe de tu sangre ya no [A]tendrá sed [B7]ja[E]más. ¤""",
"C0136": """[D]En una tarde suave, Jesús [G]al templo mar[D]chó
[D]para enseñar a la gente, an[G]siosa de oír su [A7]voz.
[D]En tanto los adoctrinaba, llega[G]ron los fari[D]seos
[D]junto con los escribas y [G]una mujer entre [A7]ellos.
[D]“Esta mujer, buen maestro, sorpren[G]dida en adul[D]terio.
[A7]Moisés dice que se lapide, ¿qué dices tú de [D]ello?”
[D]Baja la mirada a la arena y en ella es[G]cribe con el [D]dedo;
[D]es la ocasión de acusarle si se a[G]piada de aquel [A7]reo.
[D]Endereza su figura y exclama [G]en tono se[D]reno:
[D]“El que libre esté de pecado que co[G]mience el ape[A7]dreo”.
[D]Jesús inclínose de nuevo mientras [G]dibuja en el [D]suelo,
[A7]y uno a uno todos marchan, tanto mozos como [D]viejos.
[D]Y ya Jesús solo ha que[G]dado, y a [A7]la mujer dice se[D]reno:
[D]“Si el pueblo no te ha conde[G]nado, yo tam[A7]poco te con[D]deno;
[D]vete y no peques [G]más, que [A7]tienes derecho al [D]cielo”.""",
"C0137": """¤ [D]Yo soy el [A7]Buen [D]Pastor y conozco a [G]mis [A]ovejas,
[D]y todas las [A7]del redil [D]me [G]conocen a [A7]mí.
[D]Del redil la [A7]puerta soy, [D]dejo entrar a [G]mis [A]ovejas;
[D]ellas conocen mi [A7]voz, es la [D]voz de su [G]Pas[A7]tor[D].
[D]Al redil del [G]cielo se [A]entra por la [D]puerta,
[G]si es por otra [Em7]parte, eres un [A]la[A7]drón. ¤
[D]El que viene hacia [G]mí tendrá [A]vida abun[D]dante;
[G]yo mi vida entregaré por las [A]reses del [A7]redil. ¤
[D]También tengo otras [G]ovejas que no son de este [A]apris[D]co;
[G]a ellas debo apacentar, y ellas oirán mi [A]voz[A7]. ¤""",
"C0138": """¤ [E]Rezaré, [Am]pediré, [E]porque el [Am]mundo [E]no cambie [Am]mi [B]vida;
[Am]buscaré, [E]seguiré, [Am]la verdad [E]en mi [B]cora[E]zón.
[E]Que la fe [Am]en mi Dios [E]no se cambie [Am]con los [E]contra[Am]tiem[B]pos.
[Am]Pensaré [E]que el Señor [Am]a quien [E]quiere le [B]hará pade[E]cer. ¤
[B]Que los baches que tiene el [E]sendero no des[B]víen mi cami[E]nar.
[E7]Que al final de mi vida [Am]presente mis [E]manos colmadas de [Am]a[B]fán. ¤""",
"C0139": """[D]Olvidáos de la ley del [A7]Talión y [D]vivid solamente el [G]amor,[A]
[G]practicad la bondad, olvidad el [D]rencor y [G]veréis el rostro de [D]Dios.[G][A]
¤ [D]Amáos todos, nos dice el [G]Señor, como él nos [D]amó, como yo os [G]amé,[A7]
[D]y si vivo el ruego del [G]Señor, ¡qué feliz se[D]ré, qué feliz se[G]ré![A][D]
[D]Por los frutos os conoce[A7]rán, verán que mis discí[D]pulos [G]sois,[A]
[G]si os tuviéreis amor, practicando el per[D]dón, ensalzando la [G]gloria de [D]Dios.[G][A]
¤
[D]Sólo harás en el mundo el [A7]bien, corrigiendo a aquel que haga el [G]mal.[A]
[G]Es mejor sonreír, no es bueno pelliz[D]car, que la luz para [G]todos sea i[D]gual.[G][A] ¤""",
"C0140": """[Gm]Llegada a Jesús la [Eb]hora de la [D7]vuelta [Cm]hacia el [D7]Padre[Gm],
[Eb]al extremo amó a los [D7]suyos [Cm]porque [D7]nunca le olvidasen[Gm].
[Eb]El diablo obró sobre Judas [D7]el deseo [Cm]de entre[D7]garle[Gm],
[Cm]mas, sabiéndolo Jesús, [Gm]obró para que le [D7]imi[Gm]tasen.
[Gm]Se quitó el manto, se ciñó el [Cm]lienzo, tomó las [F]aguas,
[Ebdim]las echó al barreño, [Gm]lavó su pies, se [Cm]sintió [D7]sier[Gm]vo.
[Gm]Llegado al lugar de [Eb]Pedro, se [D7]niega [Cm]por no en[D7]tenderlo[Gm].
[Eb]“No me lavarás tú los [D7]pies, [Cm]consentir [D7]esto no puedo”[Gm].
[Eb]“Si no te lavo los [D7]pies [Cm]nuestros lazos [D7]romperemos”[Gm].
[Cm]A lo que Pedro respondió: [Gm]“No los pies, todo el [D7]cuer[Gm]po”.
[Gm]“Yo soy el Señor, yo soy el [Cm]Maestro: lavo los [F]pies para dar ejemplo.
[Ebdim]Hacedlo vosotros, [Gm]como yo lo he [Cm]he[D7]cho”[Gm].""",
"C0141": """[D]Yo soy la vid ver[A7]dadera, soy viña[D]dor.
[A7]A quienes viven conmigo, [D]les tengo a[D7]mor.
[G]El sar[A7]miento da [D]fruto [G]unido a [A7]la [D]vid,
[G]si tú [A7]vives con[D]migo, [G]yo vi[A7]viré en [D]ti.
[D]Si te [A7]vas de [D]mí, nada [A7]haré por [D]ti,
[A7]al vivir en [D]mí, [A7]yo seré de [D]ti.
[D]Como el Padre me [A7]ama, os amo [D]yo.
[A7]Si guardas mis mandamientos, [D]vives mi a[D7]mor.
[G]Como [A7]guardo el man[D]dato [G]que a mí [A7]se me [D]dio,
[G]perma[A7]nezco en el [D]Padre, [G]yo vivo [A7]en su a[D]mor.
[D]Tú se[A7]rás feliz al [D]vivir [A7]en [D]mí,
[A7]tú tendrás mi a[D]mor al [A7]vivir en [D]Dios.""",
"C0142": """[Am]“En un tiempo ya no me ve[Dm]réis, mas muy [G]pronto estaré a[C]quí”.
[Am]Los discípulos se hacen pre[Dm]guntas, no le entienden, [Am]¿qué quiere de[E7]cir?
[Am]Cristo sabe de su confu[Dm]sión, que entre ellos [G]nunca entende[C]rán.
[Am]Les dirige la palabra y [Dm]dice: “En verdad os [Am]digo, en ver[E7]dad...
[A]Vosotros llo[A7]raréis, el [D]mundo canta[E7]rá,
[A]vosotros sufri[A7]réis triste[D]zas y en [A]gozo [D]cambia[E7]rán.
[A]Las madres en el [A7]parto se an[D]gustian de do[E7]lor,
[A]mas al dar a [A7]luz al [D]niño se [A]llenan de a[E7]mor[A].
[A]Cuanto pidáis al [A7]Padre, él [D]lo concede[E7]rá.
[A]Hasta ahora nada ha[A7]béis pe[D]dido, mas [A]nunca olvi[D]dad[E7]:
[A]Siempre junto a vo[A7]sotros pre[D]sente esta[A]ré[D][E7],
[A]por los siglos de los [A7]siglos, [D]aquí [A]reina[E7]ré”[A].""",
"C0143": """[Cm]¡Salve, Rey de los Judíos!, ningún delito en[Gm]cuentro en [Cm]ti,
[G7]porque nada tú has hecho ¡vas a mo[Cm]rir![C7]
[Fm]Te han coronado de espinas, de loco te han puesto el [Cm]manto[C7].
[Fm]Al pueblo dice Pilato: “Ved como Cristo ha que[Cm]dado”[G7].
[Cm]“¡Crucifí[G7]cale! ¡Crucifí[Cm]cale!”
[Cm]Al pueblo ha sido entregado, han apresado a [Gm]Je[Cm]sús,
[G7]y en su espalda le han cargado con el peso de la [Cm]cruz[C7].
[Fm]Es tu pecado y el mío, tu maldad, mi ingrati[Cm]tud[C7],
[Fm]hemos huido a la tiniebla, no queremos ver la [Cm]luz[G7].
[Cm]¡Cristo va a mo[G7]rir, Cristo va a mo[Cm]rir! [G7]Por ti, por [Cm]mí.
[G7]“¡Crucifí[Cm]cale! [G7]¡Crucifí[Cm]cale! [G7]¡Crucifí[Cm]cale!”""",
"C0144": """[A7]¤ ¡Aleluya, [D]Aleluya, el [A]Señor [E7]resu[A]citó!
[A]El Señor resu[E]citó, cantad [E7]con ale[A]gría,
[A7]demos gracias al [D]Señor. ¡Ale[A]lu[E7]ya! [A]¤
[A]Mi pecado redi[E]mió Cristo Dios [E7]subiendo al [A]cielo,
[A7]nueva vida ahora [D]tengo. ¡Ale[A]lu[E7]ya! [A]¤
[A]Ahora tengo la espe[E]ranza de que Dios [E7]siempre per[A]dona,
[A7]que Cristo no me aban[D]dona. ¡Ale[A]lu[E7]ya! [A]¤
[A]Jesucristo que sube al [E]cielo, nos manda [E7]que le que[A]ramos
[A7]en todos nuestros her[D]manos. ¡Ale[A]lu[E7]ya! [A]¤""",
"C0160": """¤ [Am]¡No, no hay [G]sitio! [C]¡No, no hay [E]sitio! [Am]¡No, no hay [Dm]sitio! ¡[Am]No!
[Dm]No hay sitio donde na[Am]cer [Dm]ni lugar donde vi[Am]vir,
[Dm]para el Señor de la Vi[Am]da, [E]ni tampoco hay sitio en [Am]mí. ¤
[Dm]Cual posadero me [Am]porto [Dm]y mis puertas yo le [Am]cierro,
[Dm]y al mismo Dios de la vi[Am]da, [Dm]por mi egoísmo, no en[Am]cuentro. ¤
[Dm]Abre tus puertas, a[Am]migo, [Dm]que el mismo Dios es quien [Am]llama,
[Dm]no te pierdas que en ti [Am]entre, [E]no te pierdas que en ti [Am]nazca. ¤""",
"C0162": """[C]Las aves parecen dor[G7]mir, al cielo no se ven vo[C]lar,
las [Am]flores [Em]parecen [F]perder su [C]color, su color [F]palideció [G7]ya.
[C]Secóse el agua del [G7]mar, el fuego del sol se a[C]pagó,
los [Am]cantos del [Em]niño [F]parecen mar[C]char, [F]perdiéndose su [G7]dulce [C]voz.
¤ [C]Y es porque en el [G7]mundo se perdió el amor
y la gente humilde a[C]guarda al Salvador.
[C7]Suenen las campanas, ¡[F]campanas, sonad!
[G7]que el Rey de los Cielos ha [C]nacido ya.
La [C]vida a los campos [G7]llegó al mismo tiempo que en Be[C]lén,
las [Am]flores re[Em]nacen, las [F]aves tam[C]bién, el [F]sol ya vuelve a ca[G7]lentar.
Y [C]sobre el cauce del [G7]mar, una campanita so[C]nó,
de [Am]nuevo las [Em]aguas [F]fueron a su [C]ser y en la [F]orilla un [G7]niño [C]cantó. ¤""",
"C0163": """[E]Abro por [A]vez [E]primera [A]mis ojos [B7]en esta [E]tierra:
[A]veo son[B7]reír a mi [E]madre y a [C#m]José que [G#m]está a su [C#m]vera.
[A]Un lucerito pe[B7]queño [E]por la ventana se [C#m]cuela,
[F#m]viene a [B7]mostrarme [E]su gozo por mi [B7]llegada a la [E]tierra.
[E]Jugaré [A]con los [E]luceros y con [A]toda la [F#m]crea[B7]ción;
[A]me gozaré [B7]de las [E]cosas que mi [A]Padre [F#m]nos de[B7]jó.
[F#m]Y diré a los cuatro [A]vientos, de pequeño [B7]y de ma[E]yor,
[A]que seré [B7]amigo de [E]todos y [B7]moriré por [E]amor.
[E]Pude [A]venir a la [E]tierra siendo [A]hombre [B7]ya ma[E]yor,
[A]mas tuve [B7]miedo no [E]ser lo que de [C#m]mí [G#m]quiso [C#m]Dios.
[A]Sólo los niños [B7]verán todo [E]el mensaje de [C#m]Dios,
[F#m]por ello [B7]me hice [E]niño, y no [B7]quise venir ma[E]yor.
[E]Aunque los [A]hombres [E]olviden que [A]yo soy el [F#m]Salva[B7]dor,
[A]en este [B7]pesebre [E]humilde comienzo [A]a darles [F#m]mi a[B7]mor.
[F#m]Y si alguno comprendió [A]por qué en un portal [B7]na[E]cí,
[A]viva como [B7]yo lo [E]hice [A]y muera como [B7]yo mo[E]rí.""",
"C0164": """[E]Un villancico al [B7]Niño Je[E]sús [A]vamos [B7]a can[E]tar,
y a su madre, la [A]Virgen [B7]María, y a su [E]padre, [A]San [B7]José.
[A]Con chinchines y [E]campanitas [A]vamos [B7]al por[E]tal.
[E]Sonreiré cuando [B7]esté junto a [E]ti, y lo haré porque [A]quiero ser tu a[B7]migo;
[A]que me enseñes a ser [B7]pobre como [E]tú, [A]y será mi [B7]mejor vi[E]llancico. ¤
[E]Cuando esté en tu [B7]portal de Be[E]lén, [A]pediré que oiga [B7]cuanto digas,
[A]y después tam[B7]bién te pedi[E]ré [A]que lo sepa [B7]cantar con mi [E]vida. ¤"""
}

EXPECTED_EXISTING = {"C0001", "C0002", "C0006", "C0009", "C0010"}

con = sqlite3.connect(DB)
try:
    con.execute("PRAGMA foreign_keys=ON")
    current = {r[0] for r in con.execute("SELECT cancion_id FROM cancion WHERE TRIM(COALESCE(acordes,'')) <> ''")}
    if not EXPECTED_EXISTING.issubset(current):
        raise SystemExit(f"Faltan acordes ya importados: {sorted(EXPECTED_EXISTING-current)}")
    missing = [cid for cid in CHORDS if con.execute("SELECT 1 FROM cancion WHERE cancion_id=?", (cid,)).fetchone() is None]
    if missing:
        raise SystemExit(f"IDs inexistentes en cancion: {missing}")
    for cid, chords in CHORDS.items():
        con.execute("UPDATE cancion SET acordes=? WHERE cancion_id=?", (chords, cid))
    con.commit()

    integrity = con.execute("PRAGMA integrity_check").fetchone()[0]
    fk = con.execute("PRAGMA foreign_key_check").fetchall()
    if integrity != "ok" or fk:
        raise SystemExit(f"Validación SQLite falló: integrity={integrity}, fk={fk[:10]}")
    imported = {r[0] for r in con.execute("SELECT cancion_id FROM cancion WHERE TRIM(COALESCE(acordes,'')) <> ''")}
    expected = EXPECTED_EXISTING | set(CHORDS)
    if not expected.issubset(imported):
        raise SystemExit(f"No quedaron importadas: {sorted(expected-imported)}")
    if len(imported) != 25:
        raise SystemExit(f"Se esperaban exactamente 25 canciones con acordes y hay {len(imported)}")
finally:
    con.close()

sha = hashlib.sha256(DB.read_bytes()).hexdigest()
info = json.loads(VERSION.read_text(encoding="utf-8"))
if info.get("dataVersion") != "2026.09.30.4":
    raise SystemExit(f"Versión base inesperada: {info.get('dataVersion')}")
info.update({
    "dataVersion": "2026.09.30.5",
    "schemaVersion": 11,
    "sha256": sha,
    "date": "2026-09-30",
    "notes": "Segundo lote de acordes: 20 canciones aprobadas (C0011, C0014, C0015, C0130, C0131, C0133, C0135-C0144, C0160, C0162-C0164). Total: 25 canciones con acordes."
})
VERSION.write_text(json.dumps(info, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print(f"OK: 20 nuevas; total 25; dataVersion={info['dataVersion']}; sha256={sha}")
