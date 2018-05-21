##!/usr/bin/env bash
curl -X PUT 'http://localhost:9200/music'
curl -X PUT 'http://localhost:9200/music/song/_mapping' -d '
{
    {
        "properties" : {
            "name" : { "type" : "string" },
            "suggest" : { 
                "type" : "completion",
                "analyzer" : "simple",
                "search_analyzer" : "simple",
                "payloads" : true
            }
        }
    }
}'


curl -X PUT 'http://localhost:9200/music/song/1?refresh=true' -d '{
    "name" : "Nevermind",
    "suggest" : {
        "input": [ "Nevermind", "Nirvana" ],
        "output": "Nirvana - Nevermind",
        "payload" : { "artistId" : 2321 },
        "weight" : 34
    }
}'


curl -X POST 'http://localhost:9200/music/_suggest?pretty' -d '{
    "song-suggest" : {
        "text" : "n",
        "completion" : {
            "field" : "suggest"
        }
    }
}'