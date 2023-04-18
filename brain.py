import weaviate
from config import Config

cfg = Config()

class Schema:
    def __init__(self, class_name, vectorizer, properties) -> None:
        self.class_obj = {
            "class": class_name,
            "vectorizer": vectorizer,
            "properties": properties,
        }
        self.class_name = class_name
        self.vectorizer = vectorizer
        self.properties = properties
    
    def __dict__(self):
        return self.class_obj

class DocumentsSchema(Schema):
    def __init__(self) -> None:
        properties = [
            {
                "dataType": ["text"],
                "description": "The document text",
                "name": "document_text",
            },
        ]
        super().__init__("Documents", cfg.vectorizer, properties)

class Brain:
    """
    A general class representing a brain. A brain is a vector dataase that stores
    knowledge and can be queried to answer questions.
    """
    instance = None
    def __init__(self, endpoint, schema:Schema = DocumentsSchema()) -> None:
        self._init_client(endpoint)
        self._add_schema(schema)


    def _init_client(self, endpoint):
        self.client = weaviate.Client(
            url = endpoint,  
            additional_headers = {
                "X-OpenAI-Api-Key": cfg.openai_api_key  # Replace with your API key
            }
        )
    
    def _add_schema(self, schema:Schema = DocumentsSchema()):
        schemas = self.client.schema.get()
        schema_classes = [class_dict['class'] for class_dict in schemas['classes']]
        if schema.class_name in schema_classes:
            return
        
            
        self.client.schema.create_class(schema.__dict__())

    def _remove_schema(self, schema:Schema):
        schemas = self.client.schema.get()
        schema_classes = [class_dict['class'] for class_dict in schemas['classes']]
        if schema.class_name in schema_classes:
            self.client.schema.delete_class(schema.class_name)
    
    @staticmethod
    def get(endpoint):
        if not Brain.instance:
            Brain.instance = Brain(endpoint)
        return Brain.instance

    def add_data(self, data, schema:Schema = DocumentsSchema()):
        with self.client.batch as batch:
            batch.batch_size=100
            for i, d in enumerate(data):
                properties = {}
                for prop in schema.properties:
                    properties[prop['name']] = d[prop['name']]

                self.client.batch.add_data_object(properties, schema.class_name)


BrainInstance = Brain.get(cfg.endpoint)


def main():
    data = [
        {"document_text": """`Alexander III of Macedon (Ancient Greek: Ἀλέξανδρος, romanized: Alexandros; 20/21 July 356 BC – 10/11 June 323 BC), commonly known as Alexander the Great,[a] was a king of the ancient Greek kingdom of Macedon.[a] He succeeded his father Philip II to the throne in 336 BC at the age of 20, and spent most of his ruling years conducting a lengthy military campaign throughout Western Asia and Egypt. By the age of 30, he had created one of the largest empires in history, stretching from Greece to northwestern India.[2] He was undefeated in battle and is widely considered to be one of history's greatest and most successful military commanders.[3][4]
        
        Until the age of 16, Alexander was tutored by Aristotle. In 335 BC, shortly after his assumption of kingship over Macedon, he campaigned in the Balkans and reasserted control over Thrace and Illyria before marching on the city of Thebes, which was subsequently destroyed in battle. Alexander then led the League of Corinth, and used his authority to launch the pan-Hellenic project envisaged by his father, assuming leadership over all Greeks in their conquest of Persia.[5][6]
        
        In 334 BC, he invaded the Achaemenid Persian Empire and began a series of campaigns that lasted for 10 years. Following his conquest of Asia Minor, Alexander broke the power of Achaemenid Persia in a series of decisive battles, including those at Issus and Gaugamela; he subsequently overthrew Darius III and conquered the Achaemenid Empire in its entirety.[b] After the fall of Persia, the Macedonian Empire held a vast swath of territory between the Adriatic Sea and the Indus River. Alexander endeavored to reach the "ends of the world and the Great Outer Sea" and invaded India in 326 BC, achieving an important victory over Porus, an ancient Indian king of present-day Punjab, at the Battle of the Hydaspes. Due to the demand of his homesick troops, he eventually turned back at the Beas River and later died in 323 BC in Babylon, the city of Mesopotamia that he had planned to establish as his empire's capital. Alexander's death left unexecuted an additional series of planned military and mercantile campaigns that would have begun with a Greek invasion of Arabia. In the years following his death, a series of civil wars broke out across the Macedonian Empire, eventually leading to its disintegration at the hands of the Diadochi.
        
        With his death marking the start of the Hellenistic period, Alexander's legacy includes the cultural diffusion and syncretism that his conquests engendered, such as Greco-Buddhism and Hellenistic Judaism. He founded more than twenty cities, with the most prominent being the city of Alexandria in Egypt. Alexander's settlement of Greek colonists and the resulting spread of Greek culture led to the overwhelming dominance of Hellenistic civilization and influence as far east as the Indian subcontinent. The Hellenistic period developed through the Roman Empire into modern Western culture; the Greek language became the lingua franca of the region and was the predominant language of the Byzantine Empire up until its collapse in the mid-15th century AD. Greek-speaking communities in central Anatolia and in far-eastern Anatolia survived until the Greek genocide and Greek–Turkish population exchanges of the early 20th century AD. Alexander became legendary as a classical hero in the mould of Achilles, featuring prominently in the historical and mythical traditions of both Greek and non-Greek cultures. His military achievements and unprecedented enduring successes in battle made him the measure against which many later military leaders would compare themselves,[c] and his tactics remain a significant subject of study in military academies worldwide.[7]`"""},
        {"document_text": """Gaius Julius Caesar (/ˈsiːzər/; Latin: [ˈɡaːiʊs ˈjuːliʊs ˈkae̯sar]; 12 July 100 BC – 15 March 44 BC) was a Roman general and statesman. A member of the First Triumvirate, Caesar led the Roman armies in the Gallic Wars before defeating his political rival Pompey in a civil war, and subsequently became dictator from 49 BC until his assassination in 44 BC. He played a critical role in the events that led to the demise of the Roman Republic and the rise of the Roman Empire.
        
        In 60 BC, Caesar, Crassus, and Pompey formed the First Triumvirate, an informal political alliance that dominated Roman politics for several years. Their attempts to amass power as Populares were opposed by the Optimates within the Roman Senate, among them Cato the Younger with the frequent support of Cicero. Caesar rose to become one of the most powerful politicians in the Roman Republic through a string of military victories in the Gallic Wars, completed by 51 BC, which greatly extended Roman territory. During this time he both invaded Britain and built a bridge across the Rhine river. These achievements and the support of his veteran army threatened to eclipse the standing of Pompey, who had realigned himself with the Senate after the death of Crassus in 53 BC. With the Gallic Wars concluded, the Senate ordered Caesar to step down from his military command and return to Rome. In 49 BC, Caesar openly defied the Senate's authority by crossing the Rubicon and marching towards Rome at the head of an army.[3] This began Caesar's civil war, which he won, leaving him in a position of near unchallenged power and influence in 45 BC.
        
        After assuming control of government, Caesar began a program of social and governmental reforms, including the creation of the Julian calendar. He gave citizenship to many residents of far regions of the Roman Republic. He initiated land reform and support for veterans. He centralized the bureaucracy of the Republic and was eventually proclaimed "dictator for life" (dictator perpetuo). His populist and authoritarian reforms angered the elites, who began to conspire against him. On the Ides of March (15 March) 44 BC, Caesar was assassinated by a group of rebellious senators led by Brutus and Cassius, who stabbed him to death.[4][5] A new series of civil wars broke out and the constitutional government of the Republic was never fully restored. Caesar's great-nephew and adopted heir Octavian, later known as Augustus, rose to sole power after defeating his opponents in the last civil war of the Roman Republic. Octavian set about solidifying his power, and the era of the Roman Empire began.
            
        Caesar was an accomplished author and historian as well as a statesman; much of his life is known from his own accounts of his military campaigns. Other contemporary sources include the letters and speeches of Cicero and the historical writings of Sallust. Later biographies of Caesar by Suetonius and Plutarch are also important sources. Caesar is considered by many historians to be one of the greatest military commanders in history.[6] His cognomen was subsequently adopted as a synonym for "Emperor"; the title "Caesar" was used throughout the Roman Empire, giving rise to modern descendants such as Kaiser and Tsar. He has frequently appeared in literary and artistic works, and his political philosophy, known as Caesarism, has inspired politicians into the modern era."""},
        ]
    BrainInstance.add_data(data)

if __name__ == "__main__":
    BrainInstance._remove_schema(DocumentsSchema())
    BrainInstance._add_schema(DocumentsSchema())
    main()