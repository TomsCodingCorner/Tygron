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
    Train a new Mask R-CNN instance segmentation model.

    Parameters:
    -----------
    trainDirectory : str
        Path to the training dataset directory.
    testDirectory : str
        Path to the testing dataset directory.
    modelName : str
        Name to assign to the trained model.
    epochs : int
        Number of training epochs.
    labels : list[str]
        List of label names for the classes. Include ["parkeerplaatsen"] if only one class is present.
    augment_data : bool
        Whether to apply data augmentation (image transforms) during training.
    model_path : str
        Directory path where the trained model will be saved.
    save_interval : int, optional
        Interval (in epochs) to save the model during training; 0 means save only at the end. Default is 0.
    maskdata : list[float], optional
        List of three floats: [scoreThreshold, maskThreshold, strideFraction] for ONNX metadata. Defaults to [0.2, 0.3, 0.5].
    model_description : str, optional
        Description of the model to embed in ONNX metadata. Default is "default".

    Returns:
    --------
    model : torch.nn.Module
        The trained PyTorch model in evaluation mode.
    config : Configuration
        The configuration object used for training.
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
    Load a trained Mask R-CNN model from disk.

    Parameters:
    -----------
    path : str
        File path to the saved model.
    config : Configuration, optional
        Configuration object if previously created; if None, a new default Configuration will be created.

    Returns:
    --------
    model : torch.nn.Module
        Loaded PyTorch model ready for inference.
    config : Configuration
        Configuration object associated with the loaded model.
    """
    if not config:
        config = Configuration()
    
    model = createModelInstance(config)
    loadModel(config, model, path)
    
    return model, config

def load_default_config():
    """
    Create and return a default Configuration object with standard parameters set.

    Returns:
    --------
    config : Configuration
        Configuration object initialized with default values for model and training.
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