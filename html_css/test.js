const fs  = require("fs")
const findUniqueFilenames = async(filename) => {
    const c = await fs.readFileSync(filename,"utf-8")
     console.log(c)
    let eachLine = filename.split("\n");
    let fileList = filename.split("|");
    let allRes = ""
    for (let index = 0; index < eachLine.length; index++) {
        let fileList = eachLine[index].split("|");
        let results = "";
        for (let i = 0; i < fileList.length; i++) {
        
            let file = fileList[i].split(".")[0];
            let ext = fileList[i].split(".")[1];
            
            let  start = 0
            let willAdd = true
            while(start < fileList.length){
                let cur = fileList[start].split(".")[0]

                if (fileList[start].split(".")[0] === file && start !== i) willAdd = false
                start++
            }
        
            if (willAdd){
            results += `${file}.${ext}|`
            }
           
        }
    allRes += results.slice(0,-1)+"\n"
}
    return allRes.slice(0,-1); // Remove the trailing '|'
};

console.log(findUniqueFilenames(`foo.mp3|bar.txt|baz.mp3
wub.mp3|wub.mp3|wub.mp3|wub.txt|wub.png
quux.mp3|quux.txt|thud.mp3`))