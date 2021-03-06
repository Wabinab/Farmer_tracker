# Farmer_tracker (ALPHA)

## How to use
```commandline
pip install -r requirements.txt
python -m main <your_txt_file_goes_here> 
```

Example: 
```commandline
python -m main all_accounts.txt
```

After finish, check the `current_blacklisted.yaml` for blacklisted accounts, and `current_whitelisted.txt` for 
potential whitelisted accounts. 

**Please check the [WIKI LogFile page](https://github.com/Wabinab/Farmer_tracker/wiki/Logfile) for more details
and updates, including caveats.**

Also check **output/Example_logfile.txt** for some other information on a dummy run. 
**This run is performed on the list from these two links**: 

- https://explorer.mainnet.near.org/transactions/HjC9rnBZ3GX9QGnZ5waccCuK12sYfDYXLZWUasoQpYHd
- https://explorer.mainnet.near.org/transactions/AkgrXrM6XEXUigGVgPAxFC3MmkDkPSyuAyeLvSogBXk7

which is about slightly more than 40% of the previous redeem (as #5 is not 100) people. 

**Update:** Logfile now are automatically saved to log.txt. 

## Story behind the scene

A program to search for farmers whom farm on Learn Near Club. **Note that this program isn't solving all the problem, it just provides a tentative solution that **might** solve the problem. 
Whether or not it really works still requires more experimentation and changing of methods, perhaps even abandoning this project if found not working
(or not acceptable). 

Farmers tend to farm on LNC to claim more NEAR. We want to have a program that could clear that out. Let's try some tentative measures that might work out. 

We have a program that, for each wallet address, query for all the prior transactions that had been done before. Then, we get the explorer link that have names beside them (rather than all the explorer links); as these are the ones that have transactions. We can do this by getting the names starting with "@".
Note that this is website specific. 

Internal note: might want to get the index as well, hence we can get the corresponding near explorer to check for transaction, then could be used to find transaction amount. 

Then for each of these names, remove those that are very popular and known to be more "public", like ref.finance account, or they are staking account (containing pool.v1.near for example). Then remove these from the account. The remaining are assumed to be ordinary transactions. **Then we try to find a common ancestor among these accounts**. If several account leads to this, then potentially they're farmers. 

However this still **requires human intervention, as new public popular accounts keep adding, and we want to make sure they're included.** Otherwise, if a few people play games with pixeltoken.near and we get those, we thought they're sponsored by pixeltoken.near. 

Also, we are going to **give it a rating**. The earlier the transaction, the higher the rating. Imagine a person first create account requires some fund to transfer money to this account; this most probably ancestors from the same source. This is potentially the earliest of the earliest account, but it could also be latter accounts that increase fund to this account. Basically, we want to track down the hierarchy, and perhaps cross-account transfer from farmers that might try to blur the sight of others whom are checking on their transactions. 

Then we **might introduce two threshold**. (This is a "might", as if it leads to popular account, this could be fatal to not payout to people). This is like the traffic light, red yellow green. Potentially those that are thought to be farmers will be in the red zone, based on prior experience. But it could also be if the rating is high, then they're most probably farmers (**_again, provided we do not mistake popular accounts for this_**). Then there are the yellow zones, where system also can't determine whether they're farmers or not, hence requires human intervention. Then the green are most probably not farmers. One won't be suggesting the value of the threshold here, as it's not very useful until we try and tune it out to something useful. 

## Can farmers go against this method? 
Yes. In fact, we are not tracking down people's IP address or something, hence farmer can go onto this **if they directly buy tokens rather than transfer from another account**. If I'm a farmer, I'll pay with Moonpay (or other method) for each and every account individually, and no transaction between. This allows one to stay independent of the other, blurring away from the system. The system could not determine an ancestor if there aren't any transaction between. 

Of course, we're also making the life of the farmers more miserable; and hopefully feeling miserable due to more steps required to get tokens, they'll stop farming. 

## Caveats of this method
Of course we have caveat. 

1. **The website might thought you're DDOS attacking**. Having to read hundreds of accounts from a webpage, perhaps in parallel (as serial is a bit slow), can be classified as DDOS attack by the website you're reading from; hence you might get blocked. We can pass this by having a list of whitelisted account stored on database, and they're not checked the next time. Only those never seen or not trusted are checked. And we equally can have another blacklist to store blacklisted accounts. Alternatively, if they support an API in the future (or when one found one), then we can go past this obstacle. 
2. **Cannot read from website like NEAR Explorer**: because of **lazy loading**, you require to scroll the page down to the bottom before all transaction links are made available, and our code isn't designed to do that (requires changing to support that). Even so, the first point might not pass. 
3. **Scalability issue**: Whether it's the whitelist or the blacklist, this list grows big. We haven't design the program to integrate into a database yet.
4. More caveats, please visit [the logfile where caveats are updated during implementation updates](https://github.com/Wabinab/Farmer_tracker/wiki/Logfile) that aren't thought of at the beginning.  

These are just the ones that one could think about. There may be more issues with this program; that may be listed in the future.

## On Grandparents
How do we know how to search for grandparents? Trying all permutations is a waste of time, and one still tries to think how to solve this properly. By human intervention, this might be one way to deal with: 

Example with the previous runs, there are two accounts called `nearmarketcap.near` and `tottenham.near`. If you check their transactions, we can link them to `icebear.near` as the common parent, and then `icebear.near` can link to `7747991786f445efb658b69857eadc7a57b6b475beec26ed14da8bc35bb2b5b6`, the most "strongest" farmer on LNC website based on the subset of data. But this isn't at all too important: we already know `nearmarketcap.near` and `tottenham.near` are farmers, so there's no point? Unless they're not considered farmers, then only tracking down their ancestors give us some advantage to catch whitelisted farmers. 

Another thing we can do is to blacklist these ancestors and track from their root. Before money distribution, track down from `7747991786f445efb658b69857eadc7a57b6b475beec26ed14da8bc35bb2b5b6` downwards through all their child and mark all those as farmers account, then blacklist them just before signup starts. That could be another way, **though we still need to go through the permutations, which might be expensive**. 

If you have any other thoughts on how to solve this, welcome to post on the [specific "Discussions" channel](https://github.com/Wabinab/Farmer_tracker/discussions/5)