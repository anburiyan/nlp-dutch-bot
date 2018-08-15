# DUTCH bot

<img src="https://github.com/anburiyan/nlp-dutch-bot/blob/master/result.png" height=300px/>

## Setup
1. Create virtualenv
    Please look this site - https://virtualenv.pypa.io/en/stable/userguide/
2. if you are using Ubuntu
    `pip install -r requirement.txt`

3. If you are using windows machine
    `pip install -r requirement.txt`
    The above command will fail for few packages like `mitie`.
    So you have to install the following packages manually
    `pip install numpy,scipy,sklearn,spacy`    

4. You will have below parts in this projects
    1. Brain    

    This part takes care of Natural language understanding. It will recall all information which are stored on brain
    and response back to human.
    As of now, it can able to get person's information, their siblings and electronic device handling like switch ON/OFF

    2. Web(Human Interface)

    This is a flask application which use to interact human with DUTCH    

5. As pre-requists, you need to train this dutch to do that you need two json files `config`  and `training_data`.
    config - to train the model using either mitie or spacy
    training_data - contains data about what the dutch can able to do for you

6. To train your model you can use either `spacy` or `mitie` algorithm. For my application I am using mitie.

    1. If you are using `mitie` you should download a `.dat` file from
        https://github.com/mit-nlp/MITIE/releases/download/v0.4/MITIE-models-v0.2.tar.bz2

    2. configuration file format
        https://nlu.rasa.com/pipeline.html#mitie-sklearn

    `python -m rasa_nlu.train -c config_mitie.json`

    This step will take times based on your machine configuration

7. Once the training is done you will have a `models` folder will be created with a timestamp and given name

8. Now you are ready to configure this model with rasa-nlu

    `python -m rasa_nlu.server -c config_mitie.json --server_model_dirs=./model_YYYYMMDD-HHMMSS`

9. To setup the knowledge base for the DUTCH,
    1. Create sqlite db using these files `creation_script.sql` and `insert.sql`. 
        Use this link for sqlite DB studio http://sqlitebrowser.org/
    2. Export the created sqlite db and keep that file inside `brain` folder
    3. Use `config.py` file to define all required configurations

10. train dutch data

    `python -m rasa_nlu.train -d "/brain/data/dutch-data.json" -c "/brain/config_mitie.yml" --project "dutch" -o "/models/nlu"`

11. run rasa_nlu server

    `python -m rasa_nlu.server --path "/models/nlu" -c "/brain/config_mitie.yml"`
    
    Test the rasa_nlu server
        http://localhost:5000/parse?q=who are you&project=dutch&model=model_20180706-222616

12. Done! :). Now you are ready to get converation with your dutch

    `python boot.py`

Cheers!!

# Future work:
- The electronic device handling part is in-progress. It will connect with a raspi hardware and will do based on sending command to the hardware like switch ON/OFF computer, lights, TV, etc.,

Keep watch...
