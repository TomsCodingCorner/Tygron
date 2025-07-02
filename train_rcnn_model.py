# Required imports
from libraries.inference_training import Configuration, ImageDataset
from libraries.inference_training import initCudaEnvironment, createTransforms
from libraries.inference_training import exportOnnxModel, writeONNXMeta, loadONNX
from libraries.inference_training import trainModel, saveModel, loadModel
from libraries.inference_training import createModelInstance, testInference
from libraries.engine import evaluate
import libraries.utils as utils
import torch
import os
import random

# Initialize CUDA environment
initCudaEnvironment(numCudaDevices=1,
                    visibleCudaDevices="0", 
                    clearCudaDeviceCount=False)

def createModel(trainDirectory: str, testDirectory: str, modelName: str, epochs: int, labels: list[str], augment_data: bool, model_path: str, save_interval=0, maskdata=None, model_description="default"):
    """
    Train a new Mask R-CNN model
    
    :param trainDirectory: path naar training dataset
    :param testDirectory: path naar testing dataset
    :param modelName: naam van model 
    :param epochs: hoeveelheid epochs
    :param labels: list van labels, geef normaal ["parkeerplaatsen"] als er geen andere objecten zijn
    :param augment_data: bepaald of er image transforms gedaan worden
    :param model_path: path naar save locatie van model
    :param save_interval: save model every N epochs (0 = only at end)
    :param maskdata: [score_threshold, mask_threshold, stride_fraction]
    :param model_description: beschrijft het model in de ONNX als het gesaved is
    :return: trained model and configuration
    """
    if maskdata is None:
        maskdata = [0.2, 0.3, 0.5]
        
    config = Configuration()
    print("Device: " + str(config.device))
    
    # Configure model settings
    config.setSaveInterval(save_interval)
    config.setSavePath(model_path)
    config.setIsCrowd(False)
    config.setDatasetPaths(trainPath=trainDirectory, testPath=testDirectory)
    config.setFilePrefix("")
    config.setModelName(modelName)
    config.setInputSizes(inputWidth=250, inputHeight=250)
    config.setInputCellSize(cellSizeM=0.25, minCellSizeM=0.1, maxCellSizeM=0.5)
    config.setVersion(20250121)
    config.setModelInfo(channels=3, numClasses=len(labels)+1,  # (+1 for background)
                        bboxOverlap=True, bboxPerImage=250, reuseModel=False)
    config.setEpochs(epochs)
    config.setOnnxInfo(producer="Tygron", description=model_description)
    
    # Add legend entries
    config.addLegendEntry("Background", 0, "#00000000")
    for i, label in enumerate(labels, 1):
        color = "#" + ''.join([random.choice('ABCDEF0123456789') for _ in range(6)])
        config.addLegendEntry(label, i, color)
    
    # Set ONNX metadata
    config.setOnnxMetaData(scoreThreshold=maskdata[0],
                           maskThreshold=maskdata[1], 
                           strideFraction=maskdata[2])
    
    config.setTensorInfo(tensorName='input_A:RGB_normalized', batchAmount=1)
    
    # Create datasets
    if augment_data:
        trainingDataset = ImageDataset(config, True, createTransforms(True))
        testDataset = ImageDataset(config, False, createTransforms(False))
    else:
        trainingDataset = ImageDataset(config, True, createTransforms(False))
        testDataset = ImageDataset(config, False, createTransforms(False))
    
    print(f"Train Image count: {trainingDataset.__len__()}")
    print(f"Test Image count: {testDataset.__len__()}")
    
    # Validate datasets
    if not trainingDataset.validateFiles():
        print("Inconsistent training dataset")
    
    if not testDataset.validateFiles():
        print("Inconsistent test dataset")
    
    print("Pytorch model name: " + config.getPytorchModelFileName())
    print("ONNX file name: " + config.getOnnxFileName())
    
    # Train the model
    model = trainModel(config, trainingDataset, testDataset)
    model.eval()
    
    # Save the model
    saveModel(config, model, path=model_path + config.getPytorchModelFileName())
    
    # Export to ONNX
    exportOnnxModel(config, model, model_path)
    writeONNXMeta(config)
    
    return model, config

def load_model(path: str, config=None):
    """
    Load an existing trained model
    
    :param path: path naar model save location 
    :param config: config als het eerder is ingesteld
    :return: loaded model and configuration
    """
    if not config:
        config = Configuration()
    
    model = createModelInstance(config)
    loadModel(config, model, path)
    
    return model, config

def load_default_config():
    """
    Load default configuration settings
    """
    config = Configuration()
    config.setIsCrowd(False)
    config.setFilePrefix("")
    config.setInputSizes(inputWidth=250, inputHeight=250)
    config.setInputCellSize(cellSizeM=0.25, minCellSizeM=0.1, maxCellSizeM=0.5)
    config.setVersion(20250121)
    config.setModelInfo(channels=3, numClasses=2+1,  # (1 + background)
                        bboxOverlap=True, bboxPerImage=250, reuseModel=False)
    config.addLegendEntry("Background", 0, "#00000000")
    config.setOnnxMetaData(scoreThreshold=0.2,
                           maskThreshold=0.3,
                           strideFraction=0.5)
    config.setTensorInfo(tensorName='input_A:RGB_normalized', batchAmount=1)
    
    return config

if __name__ == "__main__":
    # Example training configuration
    train_directory = "datasets/combo_overlay_sets/train"  # Update this path
    test_directory = "datasets/combo_overlay_sets/test"    # Update this path
    modelName = "my_parking_model"
    epochs = 1
    labels = ["parkeerplaats"]  # Add your custom labels here
    augment = False  # Set to True for data augmentation
    save_path = "models/"
    
    # Create models directory if it doesn't exist
    os.makedirs(save_path, exist_ok=True)
    
    print("Starting model training...")
    print(f"Train directory: {train_directory}")
    print(f"Test directory: {test_directory}")
    print(f"Model name: {modelName}")
    print(f"Epochs: {epochs}")
    print(f"Labels: {labels}")
    
    # Train the model
    try:
        model, config = createModel(
            trainDirectory=train_directory,
            testDirectory=test_directory,
            modelName=modelName,
            epochs=epochs,
            labels=labels,
            augment_data=augment,
            model_path=save_path,
            save_interval=5,  # Save every 5 epochs
            maskdata=[0.2, 0.3, 0.5],  # Score threshold, mask threshold, stride fraction
            model_description=f"Parking space detection model trained for {epochs} epochs"
        )
        
        print("Training completed successfully!")
        print(f"Model saved to: {save_path}")
        
    except Exception as e:
        print(f"Training failed with error: {e}")
        raise