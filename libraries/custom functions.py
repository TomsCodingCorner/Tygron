from libraries.inference_training import Configuration, ImageDataset
from libraries.inference_training import initCudaEnvironment, createTransforms
from libraries.inference_training import drawImageAndFeatureMasks
from libraries.inference_training import exportOnnxModel, writeONNXMeta, loadONNX
from libraries.inference_training import trainModel, saveModel, loadModel
from libraries.inference_training import createModelInstance, testInference
from libraries.engine import evaluate
import libraries.utils as utils
import torch
import os
import random


def createModel(trainDirectory: str, testDirectory: str, modelName: str, epochs: int, labels: list[str],
                augment_data: bool, model_path: str, model_description="default"):
    """
    :param trainDirectory: path naar training dataset
    :param testDirectory: path naar testing dataset
    :param modelName: naam van model
    :param epochs: hoeveelheid epochs
    :param labels: list van labels, geef normaal ["parkeerplaatsen"] als er geen andere objecten zijn
    :param augment_data: bepaald of er image transforms gedaan worden, nog niet getest
    :param model_path: path naar save locatie van model
    :param model_description: beschrijft het model in de ONNX als het gesaved is
    :return:
    """
    config = Configuration()
    print("Device: " + str(config.device))
    config.setIsCrowd(False)
    config.setDatasetPaths(trainPath=trainDirectory, testPath=testDirectory)
    config.setFilePrefix("")
    config.setModelName(modelName)
    config.setInputSizes(inputWidth=250, inputHeight=250)
    config.setInputCellSize(cellSizeM=0.25, minCellSizeM=0.1, maxCellSizeM=0.5)
    config.setVersion(20250121)
    config.setModelInfo(channels=3, numClasses=2 + 1,  # (1 + background)
                        bboxOverlap=True, bboxPerImage=250, reuseModel=False)
    config.setEpochs(epochs)
    config.setOnnxInfo(producer="Tygron", description=model_description)
    config.addLegendEntry("Background", 0, "#00000000")
    i = 1
    for label in labels:
        config.addLegendEntry(label, i, ["#" + ''.join([random.choice('ABCDEF0123456789') for i in range(6)])])
        i += 1

    config.setOnnxMetaData(scoreThreshold=0.2,
                           maskThreshold=0.3,
                           strideFraction=0.5)

    config.setTensorInfo(tensorName='input_A:RGB_normalized', batchAmount=1)
    if augment_data:
        trainingDataset = ImageDataset(config, True, createTransforms(True))
        testDataset = ImageDataset(config, False, createTransforms(False))
    else:
        trainingDataset = ImageDataset(config, True, createTransforms(False))
        testDataset = ImageDataset(config, False, createTransforms(False))

    print("Train Image count: " + str(trainingDataset.__len__()))
    print("Test Image count: " + str(testDataset.__len__()))

    if not trainingDataset.validateFiles(False):
        print("Inconsistent training dataset ")
        trainingDataset.validateFiles(True)

    if not testDataset.validateFiles(False):
        print("Inconsistent test dataset ")
        testDataset.validateFiles(True)

    print("Pytorch model name " + config.getPytorchModelFileName())
    print("Onnx file name " + config.getOnnxFileName())

    model = trainModel(config, trainingDataset, testDataset)
    model.eval()

    saveModel(config, model, path=model_path + config.getPytorchModelFileName())

    exportOnnxModel(config, model, model_path)
    writeONNXMeta(config)

    return model, config


def load_model(path: str, config=None):
    """
    :param path: path naar model save location
    :param config: config als het eerder is ingesteld
    :return:
    """
    if not config:
        config = Configuration()

    model = createModelInstance(config)
    loadModel(config, model, path)

    return model, config


def load_default_config():
    config = Configuration()
    config.setIsCrowd(False)
    config.setFilePrefix("")
    config.setInputSizes(inputWidth=250, inputHeight=250)
    config.setInputCellSize(cellSizeM=0.25, minCellSizeM=0.1, maxCellSizeM=0.5)
    config.setVersion(20250121)
    config.setModelInfo(channels=3, numClasses=2 + 1,  # (1 + background)
                        bboxOverlap=True, bboxPerImage=250, reuseModel=False)
    config.addLegendEntry("Background", 0, "#00000000")
    config.setOnnxMetaData(scoreThreshold=0.2,
                           maskThreshold=0.3,
                           strideFraction=0.5)
    config.setTensorInfo(tensorName='input_A:RGB_normalized', batchAmount=1)

    return config