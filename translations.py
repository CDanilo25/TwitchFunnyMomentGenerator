import locale


class Translations:
    languageToUse = 'en_GB'

    labels = {
        "main_start_streamerTypeAsk": {
            "it_IT": "[0: da video; 1: da clip] Da dove genero? ",
            "en_GB": "[0: from video; 1: from clip] Where do you want to generate the video from? "
        },

        "main_start_streamerManyAsk": {
            "it_IT": ">>> Quanti elementi devo prelevare? ",
            "en_GB": ">>> How many items should I take? "
        },

        "main_start_streamerNameAsk": {
            "it_IT": ">>> Nome del canale da cui prelevare? ",
            "en_GB": ">>> Now please enter the name of the channel: "
        },

        "main_start_streamerClipPeriodAsk": {
            "it_IT": "[0: sempre; 1: 24 ore; 2: ultima settimana; 3: ultimo mese] Che periodo prelevo per le clip? ",
            "en_GB": "[0: from the start; 1: last 24h; 2: last week; 3: last month] Select the period to be considered for your clips: "
        },

        "main_error_ffmpeg": {
            "it_IT": "[!] FFMPEG non è stato trovato nel sistema. Non installato o non nel PATH?",
            "en_GB": "[!] FFMPEG has not been found on your system. Check your installation or if it is included in the PATH."
        },

        "main_error_stuff": {
            "it_IT": "Ti ho chiesto di non toccare >:(",
            "en_GB": "Stuff touched >:("
        },

        "main_exit_cleanup": {
            "it_IT": "\n>>> Pulizia...",
            "en_GB": "\n>>> Cleaning up..."
        },

        "main_vibe_check_error": {
            "it_IT": "[!] Errore nel prelevare informazioni. Problemi di rete o nome canale sbagliato?",
            "en_GB": "[!] Failed to get data. Do you have network issues or is the channel name wrong?"
        },

        "main_download": {
            "it_IT": ">>> >>> Download di {}...",
            "en_GB": ">>> >>> Downloading {}..."
        },

        "main_transition_ask": {
            "it_IT": "[0: no dai; 1: si kek] Vuoi aggiungere una transizione statica tra le clip? ",
            "en_GB": "[0: no plz; 1: yay] Do you want to add a funny transition between your clips? "
        },

        "main_repeatOperation_ask": {
            "it_IT": "[0: interrompi; 1: prosegui] Divertimento salvato. Vuoi generare altro con i video prelevati? ",
            "en_GB": "[0: stop; 1: keep going] The funny has been saved. Do you want to generate something else with the current videos? "
        },

        "vutils_video_auth": {
            "it_IT": ">>> >>> >>> Autorizzando e prelevando la playlist del video...",
            "en_GB": ">>> >>> >>> Obtaining video's playlist by authorization..."
        },

        "vutils_video_download": {
            "it_IT": ">>> >>> >>> Download dei componenti del video...",
            "en_GB": ">>> >>> >>> Downloading VOD parts..."
        },

        "vutils_video_merge": {
            "it_IT": ">>> >>> >>> Unione dei file in un video singolo...",
            "en_GB": ">>> >>> >>> Merging files in a single MP4 file..."
        },

        "vutils_video_clean": {
            "it_IT": ">>> >>> >>> Pulizia file temporanei...",
            "en_GB": ">>> >>> >>> Removing temporary files..."
        },

        "vutils_video_howMuchAsk": {
            "it_IT": ">>> Quante clip devono essere generate per ogni video scaricato? ",
            "en_GB": ">>> How many clips must be generated for each downloaded video? "
        },

        "vutils_generatingFunny": {
            "it_IT": ">>> >>> >>> Generazione del divertimento (verrà salvato in RESULT)...",
            "en_GB": ">>> >>> >>> Generating a truly funny moment (it will be saved in RESULT directory)..."
        },

        "vutils_clip_urlGen": {
            "it_IT": ">>> >>> >>> Componendo l'URL per la clip...",
            "en_GB": ">>> >>> >>> Generating the URL for the clip..."
        },

        "vutils_clip_download": {
            "it_IT": ">>> >>> >>> Download della clip...",
            "en_GB": ">>> >>> >>> Downloading clip..."
        },

        "vutils_ffmpeg_error": {
            "it_IT": "[!] FFMPEG ha riscontrato un errore nel tentativo di unire i file video.",
            "en_GB": "[!] FFMPEG returned an error while trying to merge your video."
        },

        "vutils_genFunny_stats": {
            "it_IT": ">>> >>> >>> >>> Clip numero {} | partenza: {}s | fine: {}s",
            "en_GB": ">>> >>> >>> >>> Clip #{} | starting time: {}s | ending time: {}s"
        }

    }

    def __init__(self):
        valid_languages = ["en_GB", "it_IT"]
        system_language = locale.getdefaultlocale()[0]
        if system_language in valid_languages:
            self.languageToUse = system_language

    def get(self, label):
        try:
            return self.labels[label][self.languageToUse]
        except KeyError:
            return "--- Missing label '{}' ---".format(label)
