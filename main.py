import os
from random import randint
from recognition import train, predict, save_image_with_blur

NAME_TRAINED_MODEL = "trained_model.clf"
PATH = "img"
PATH_TRAIN = "img/train"
PATH_TEST = "img/test"

if __name__ == "__main__":
    os.chdir(os.path.dirname(os.path.realpath(__file__)))
    if not os.path.exists(PATH) and not os.path.exists(PATH_TRAIN) and not os.path.exists(PATH_TEST):
        print("Error! directory or subdirectory img doesn't exist (need img/train AND img/test)!\nPlease create it and/or see documentation at https://github.com/av1m/blur_face_recognition/")
        import sys
        sys.exit(0)

    # STEP 1: Train and save it to disk
    if not os.path.exists(NAME_TRAINED_MODEL):
        print("Training ...")
        classifier = train(PATH_TRAIN, model_save_path=NAME_TRAINED_MODEL, n_neighbors=2)
        print("Training complete!\nFile written : {}".format(NAME_TRAINED_MODEL))
    else: # If the model is trained and saved, we just use it
        print("File {} exist ! \nAlready Trained!".format(NAME_TRAINED_MODEL))

    # STEP 2 : Create path for new file : 
    path_save = os.path.join(PATH, "output")
    if not os.path.exists(path_save): os.makedirs(path_save)
    else: 
        path_save = path_save+"_{}".format(randint(0, 99999))
        os.makedirs(path_save)

    print("OUTPUT Directory : {}".format(path_save))

    # STEP 3: Using the trained classifier, make predictions for unknown images
    for image_file in os.listdir(PATH_TEST):
        full_file_path = os.path.join(PATH_TEST, image_file)

        print("Looking for faces in {}".format(image_file))

        # Find all people in the image using a trained classifier model
        # Note: You can pass in either a classifier file name or a classifier model instance
        predictions = predict(full_file_path, model_path=NAME_TRAINED_MODEL)
        
        #keys = [predict for predict in predictions if predict[0] == 'chanael']

        # Print results on the console
        for name, (top, right, bottom, left) in predictions:
            print("- Found {} at ({}, {})".format(name, left, top))

        # Display results overlaid on an image
        save_image_with_blur(image_file, PATH_TEST, path_save, predictions)
