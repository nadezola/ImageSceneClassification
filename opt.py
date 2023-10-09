# device will be recognized automatically
device = None

# Pre-trained Object Detection Model
ckpt_path = 'checkpoints'  # Path to pre-trained weights and models
obj_det_clear_pretrained_model = 'YOLOv3_clear_kitti_pretrained.pt'  # Pretrained YOLOv3 model for object detection on one image scene
obj_det_numcls = 8  # Number of object classes in pretrained model
obj_det_cls = ['Car', 'Van', 'Truck', 'Pedestrian', 'Person_sitting', 'Cyclist', 'Tram', 'Misc']  # Names of object classes in pretrained model

# Scene Classification Head
img_size = 640
batch_size = 8
CLS_SCENE = ['vienna', 'auckland', 'frankfurt', 'iceland', 'none', 'unknown']
epochs = 30
augment = False
workers = 2
