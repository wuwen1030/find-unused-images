find-unused-images
==================

Find unused images in a xcode project
###作用：
通过此脚本可以找出工程中没有引用的文件，缩减安装包的大小。
###使用方法：
命令 "python trimpackage.py .xcodeproj文件路径"，比如"python find_unused_images.py /Users/xia/Desktop/SVN_CODE/Hosting-iOS/HostingReport/Hosting/Hosting.xcodeproj "
###说明：
* 目前仅能检测 imageNamed:@"xxxx"的形式
* icon Default文件由于没有在代码中出现，因此结果是有误的，请注意不要误删
* 暂时还未支持".xib"".storyboard"引用图片检测的功能
* 对于imageNamed:@"xxxx_%d"这种形式的引用不能正确的检测

###建议：
删除文件之前最好做好确认工作