## Unused-images-finder
==================

Find the unused images in a Xcode project.

### Why `Unused_images_finder`

Today, the size of APPs are getting very large. But disk space is still expensive on iPhone. So we need to optimize the package size. Besides, as developers, we should keep the project clean, and remove the rubish resources.

### Usage
Clone or download the source file.

```
git clone git@github.com:wuwen1030/find-unused-images.git
```

Open the Terminal, run the command as follows:

```
python unused_images_finder.py PROJECT_PATH {SOURCE_PATH}
```

`PROJECT_PATH` is required, set the argument to your project file. `SOURCE_PATH` is optonal, default is the parent path of project file. We usually set this to the root path of project.

### Known issues
1. `.storyboard` & `.xib` is not supported.
2. Images which are not referred with file names directly cann't be recognized correctly. e.g
	
	```objc
	NSString *imageName = @"imageName";
	UIImage *image = [UIImage imageNamed:imageName];
	...
	UIImage *image = [UIImage imageNamed:[NSString stringWithFormat:@"xxx%d", 2]]
	```	
	
3. Miss the target
	* Icon & Launch files are not referred in the code files, which will be recognized uncorrectly.
	* Images described in the issues #2
	