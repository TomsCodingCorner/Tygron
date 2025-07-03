import torch
from torchvision import tv_tensors
from torchvision.transforms import v2
from libraries.inference_training import Configuration, ImageDataset
from libraries.inference_training import initCudaEnvironment, createTransforms


def compute_dice_score(pred_masks, gt_masks):
    """
    Compute the Dice similarity coefficient between predicted and ground truth binary masks.

    Parameters:
    -----------
    pred_masks : torch.Tensor
        Tensor of predicted binary masks (shape: [N, H, W]), where N is number of masks.
    gt_masks : torch.Tensor
        Tensor of ground truth binary masks (shape: [N, H, W]).

    Returns:
    --------
    float or None
        The average Dice score over all mask pairs. Returns None if input lists are empty.

    Notes:
    ------
    - Dice score = (2 * intersection) / (sum of sizes of both masks).
    - Handles edge cases where masks are empty.
    """
    dice_scores = []
    for pred_mask, gt_mask in zip(pred_masks, gt_masks):
        intersection = (pred_mask & gt_mask).sum().item()
        union = pred_mask.sum().item() + gt_mask.sum().item()
        if union == 0:
            dice_scores.append(1.0 if intersection == 0 else 0.0)  # Handle edge cases
        else:
            dice_scores.append(2 * intersection / union)
    if len(dice_scores) == 0:
        return None
    return sum(dice_scores) / len(dice_scores)  # Mean Dice score


def testInferenceDice(config: Configuration,
                      dataset: ImageDataset, model,
                      imageNumber: int):
    """
    Perform inference on a single image and compute the Dice score between predicted and ground truth masks.

    Parameters:
    -----------
    config : Configuration
        Configuration object containing model parameters and thresholds.
    dataset : ImageDataset
        Dataset object providing access to images and ground truth masks.
    model : torch.nn.Module
        Trained instance segmentation model for prediction.
    imageNumber : int
        Index of the image in the dataset to run inference on.

    Returns:
    --------
    float
        Dice similarity score measuring overlap between predicted and ground truth masks.

    Notes:
    ------
    - Converts dataset images to float tensors and applies evaluation transforms.
    - Model predictions are thresholded using the maskThreshold from the config.
    - Ground truth masks are binarized and resized if needed to match prediction size.
    - Uses compute_dice_score() to calculate final Dice metric.
    """
    imgs = dataset.getImages(imageNumber)
    for i in range(len(imgs)):
        imgs[i] = v2.functional.convert_image_dtype(imgs[i], dtype=torch.float)
        imgs[i] = tv_tensors.Image(imgs[i])

    img = torch.cat(imgs, 0)
    eval_transform = createTransforms(train=False)

    with torch.no_grad():
        x = eval_transform(img)
        x = x.to(config.device)
        predictions = model([x])
        pred = predictions[0]

    pred_masks = (pred["masks"] > config.maskThreshold).squeeze(1).int()
    pred_masks = pred_masks.to(config.device)

    # Get ground truth masks
    gt_masks = dataset.getMask(imageNumber)  # Adjust this to match your dataset structure
    gt_masks = (gt_masks > 0).int()  # Convert to binary masks
    gt_masks = gt_masks.to(config.device)

    # Ensure pred_masks and gt_masks have the same shape
    if pred_masks.shape != gt_masks.shape:
        gt_masks = torch.nn.functional.interpolate(
            gt_masks.unsqueeze(0).float(), size=pred_masks.shape[-2:][0], mode="nearest"
        ).squeeze(0).int()
    print(pred_masks.shape, gt_masks.shape)
    print("pred masks:", pred_masks)
    print("gt masks:", gt_masks)
    # Compute Dice score
    dice_score = compute_dice_score(pred_masks, gt_masks)

    return dice_score