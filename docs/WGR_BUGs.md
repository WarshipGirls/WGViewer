# MoeFantasy BUG's

Throughout the development of this software, numerous potential bugs of the game itself are spotted via MoeFantasy's (MF) json transmissions.
This markdown is created to document those bugs, hopefully which they will fix soon.

1.

Data version: 2020112002

If looking from `shipCard->equipmentType` route, light cruiser can equip battleships' main battery
workaround: check on `shipEquimnt->shipType` (By the way, they spell equipment wrong)

suggestion to MF: delete `equipmentType` in your `getInitConfigs->shipCard`

2. 

Data version: 2020112002

In getInitConfigs, `shipCardWu` seems identical to `shipCard`. Why wasting time and bandwidth to transmit these?

suggestion to MF: delete `shipCardWu` in your `getInitConfigs`

3. 

Data version: 2020112002

One of the equipment, see below, has seemingly invalid `effect` field. All other equipment has either "0" as default or an `dict` object. This one is an incomplete `dict` object in the form of a `str` object. It is reasonable to doubt if this particular equipment is effective or not.

```
"cid": 10033721,
"title": "空射火箭弹",
"effect": "{\"boom\":0.05,\"hit\":5",
```

suggestion to MF: use `"effect": {'boom':0.05, 'hit':5}`

4.

Game version: 5.1.0

In the response body of `six/passLevel` call, the json is invalid with boolean `False` in one of the fields:

```
	...
   "$taward":[
      False,
      False,
      False,
      False,
      {
         "20241":24
      },
      False,
      {
         "23":30
      },
      False,
      {
         "20482":5
      }
   ],
   ...
```

5. Exceeding dock limit

During Thermopylae Ex-6 sortie, if you stay in the mode without exiting, you can actually exceed the dock limit indefinitely.


![alt text](pics/bug/excess_dock.PNG)


6. Exceeding Thermopylae Ex-6 sortie ticket limit

You can stockpiling Thermopylae Ex-6 sortie tickets


![alt text](pics/bug/excess_sortie_ticket.png)

