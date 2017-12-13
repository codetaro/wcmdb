var duplicates = [];

db.news.aggregate([
    {$group: {
        _id: {title: "$title", author: "$author", add_time: "$add_time"},
        dups: {"$addToSet": "$_id"},
        count: {"$sum": 1}
    }},
    {$match: {count: {"$gt": 1}}}
],
    {allowDiskUse: true})  // for faster processing if set is larger
.forEach(function (doc) {
    doc.dups.shift();
    doc.dups.forEach(function (dupId) {
        duplicates.push(dupId);
    })
})

printjson(duplicates);

db.news.remove({_id: {$in: duplicates}})