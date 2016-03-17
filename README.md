Unused-images-finder
==================

Find the unused images in a Xcode project.

### Why `Unused_images_finder`

Today, the size of APPs are getting very large. But disk space is still expensive on iPhone. So we need to optimize the package size. Besides that, as developers, we should keep the project clean, and remove the rubbish resources.

### Usage
Clone or download the source file.

```
git clone git@github.com:wuwen1030/find-unused-images.git
```

Open the Terminal, run the command as follows:

```
python unused_images_finder.py PROJECT_PATH {SOURCE_PATH}
```

`PROJECT_PATH` is required, set the argument to your project file path. `SOURCE_PATH` is optional, default is the parent path of project file. We usually set this to the root path of project.

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
	
### More

[My blog](http://wuwen1030.github.io/2016/03/17/%E6%9F%A5%E6%89%BEXcode%E5%B7%A5%E7%A8%8B%E6%9C%AA%E4%BD%BF%E7%94%A8%E7%9A%84%E5%9B%BE%E7%89%87%E8%B5%84%E6%BA%90/)
