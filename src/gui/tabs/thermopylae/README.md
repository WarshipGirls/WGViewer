# README

Documents the meaning of json fields from server response

```
    getuserdata
        -> nodeId: current node
        -> levelId: current level
        -> chapterId: current chapter
        -> npcId: current enemy
        -> boats: last set boat
        -> level_id  (I believe this is the user reached level)
            9301 (E1 map1) 9303 (E1 map3) 9304 (E2 map1) 9316 (E6 map 1)
    node/sub map status
        - 1: pre battle (just entered the battle)
        - 2: in battle
        - 3: after battle (collected rewards)
```
