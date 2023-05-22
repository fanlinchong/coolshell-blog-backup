# coolshell-blog-backup
备份耗子叔的博客文章



## 实现方式
使用 [SingleFile](https://github.com/gildas-lormeau/SingleFile) 项目提供的[命令行工具](https://github.com/gildas-lormeau/single-file-cli)导出给定页面的为单一文件。

## 使用方式
```bash
// 在项目根目录下执行
python main.py
```
文章已经以单页的形式保存在  `articles` 目录

命名规则为 `文章id_文章标题.html`

由于文章标题中的一些字符不适合作为文件名，因此做了部分替换。

