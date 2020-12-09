# MoeFantasy BUG's

Throughout the development of this software, numerous potential bugs of the game itself are spotted via MoeFantasy's (MF) json transmissions.
This markdown is created to document those bugs, hopefully which they will fix soon.

1.

Data version: 2020112002

If looking from `shipCard->equipmentType` route, light crusier can equip battleships' main battery
workaround: check on `shipEquimnt->shipType` (By the way, they spell equipment wrong)

suggestion to MF: delete `equipmentType` in your `getInitConfigs->shipCard`

2. 

Data version: 2020112002

In getInitConfigs, `shipCardWu` seems idential to `shipCard`. Why wasting time and bandwidth to transmit these?

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

In the shop data (shown below), there are, from time to time, untoleratable mismatchings! AND, waste bandwidth on repeated data, again! 

```
{
	...
   "$pools":[
   		# shows 5 ship_ids here
   ],
   "$ssss":[
   		# only shows 4 lists here; SHOULD BE 5 (sometimes there are 5)
   		# the lists are in the form of [ship_star, ship_id, cost]
   ],
   ...
   "boats":[
   		# only shows 4 ship_ids here; SHOULD BE 5 (sometimes there are 5)
   ],
   ...
   "buyPointArr":[
   		# shows the cost of 5 ships here
   ]
   # sometimes the buff-card-id is 0
}
```