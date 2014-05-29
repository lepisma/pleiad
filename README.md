#pleiad

Experimental word classifier based on dynamic time warping

Pleiad helps you identify words in an image.
Use it when you dont need extensive character recognition and/or dont have much data, and need to identify few pre planned words only.

Pleiad **doesn't** need extensive training data, just a single image for each class (few more for better result) is all you need.

###Setup

*	Install R (and python)
*	`install.packages('dtw')` in R shell
*	`pip install -r requirements`

###Usage

*	Crop words from image and stretch to a fixed size (*one size per classifier*)
	
    ![sample](/sample_words.jpg)
    
    
*	Create `Word` objects from word images

```
from pleiad import pleaid
word = pleiad.Word(image, "climb")
```
    
*	Train classifier from a list of `Word`s

```
classifier = pleiad.PleiadClassifier(image.shape)
classifier.train(word_list)
```

*	Predict

```
classifier.predict(word)
```

*	Save for future use

```
classifier.save('classifierOne')
```

###Working

Pleiad works by treating the outer outline of each image of word as a time series and predicting by using the dynamic time warping distance between the series.

###License

MIT

Copyright (c) 2014 Abhinav Tushar