

hex_contract_dict = dict(
    name='hex',
    abi='[{"inputs":[],"payable":false,"stateMutability":"nonpayable","type":"constructor"},{"anonymous":false,' \
              '"inputs":[{"indexed":true,"internalType":"address","name":"owner","type":"address"},{"indexed":true,' \
              '"internalType":"address","name":"spender","type":"address"},{"indexed":false,"internalType":"uint256",' \
              '"name":"value","type":"uint256"}],"name":"Approval","type":"event"},{"anonymous":false,"inputs":[{' \
              '"indexed":false,"internalType":"uint256","name":"data0","type":"uint256"},{"indexed":false,' \
              '"internalType":"uint256","name":"data1","type":"uint256"},{"indexed":true,"internalType":"bytes20",' \
              '"name":"btcAddr","type":"bytes20"},{"indexed":true,"internalType":"address","name":"claimToAddr",' \
              '"type":"address"},{"indexed":true,"internalType":"address","name":"referrerAddr","type":"address"}],' \
              '"name":"Claim","type":"event"},{"anonymous":false,"inputs":[{"indexed":false,"internalType":"uint256",' \
              '"name":"data0","type":"uint256"},{"indexed":false,"internalType":"uint256","name":"data1",' \
              '"type":"uint256"},{"indexed":false,"internalType":"uint256","name":"data2","type":"uint256"},' \
              '{"indexed":true,"internalType":"address","name":"senderAddr","type":"address"}],"name":"ClaimAssist",' \
              '"type":"event"},{"anonymous":false,"inputs":[{"indexed":false,"internalType":"uint256","name":"data0",' \
              '"type":"uint256"},{"indexed":true,"internalType":"address","name":"updaterAddr","type":"address"}],' \
              '"name":"DailyDataUpdate","type":"event"},{"anonymous":false,"inputs":[{"indexed":false,' \
              '"internalType":"uint256","name":"data0","type":"uint256"},{"indexed":true,"internalType":"uint40",' \
              '"name":"stakeId","type":"uint40"}],"name":"ShareRateChange","type":"event"},{"anonymous":false,' \
              '"inputs":[{"indexed":false,"internalType":"uint256","name":"data0","type":"uint256"},{"indexed":false,' \
              '"internalType":"uint256","name":"data1","type":"uint256"},{"indexed":true,"internalType":"address",' \
              '"name":"stakerAddr","type":"address"},{"indexed":true,"internalType":"uint40","name":"stakeId",' \
              '"type":"uint40"}],"name":"StakeEnd","type":"event"},{"anonymous":false,"inputs":[{"indexed":false,' \
              '"internalType":"uint256","name":"data0","type":"uint256"},{"indexed":false,"internalType":"uint256",' \
              '"name":"data1","type":"uint256"},{"indexed":true,"internalType":"address","name":"stakerAddr",' \
              '"type":"address"},{"indexed":true,"internalType":"uint40","name":"stakeId","type":"uint40"},' \
              '{"indexed":true,"internalType":"address","name":"senderAddr","type":"address"}],' \
              '"name":"StakeGoodAccounting","type":"event"},{"anonymous":false,"inputs":[{"indexed":false,' \
              '"internalType":"uint256","name":"data0","type":"uint256"},{"indexed":true,"internalType":"address",' \
              '"name":"stakerAddr","type":"address"},{"indexed":true,"internalType":"uint40","name":"stakeId",' \
              '"type":"uint40"}],"name":"StakeStart","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,' \
              '"internalType":"address","name":"from","type":"address"},{"indexed":true,"internalType":"address",' \
              '"name":"to","type":"address"},{"indexed":false,"internalType":"uint256","name":"value",' \
              '"type":"uint256"}],"name":"Transfer","type":"event"},{"anonymous":false,"inputs":[{"indexed":false,' \
              '"internalType":"uint256","name":"data0","type":"uint256"},{"indexed":true,"internalType":"address",' \
              '"name":"memberAddr","type":"address"},{"indexed":true,"internalType":"uint256","name":"entryId",' \
              '"type":"uint256"},{"indexed":true,"internalType":"address","name":"referrerAddr","type":"address"}],' \
              '"name":"XfLobbyEnter","type":"event"},{"anonymous":false,"inputs":[{"indexed":false,' \
              '"internalType":"uint256","name":"data0","type":"uint256"},{"indexed":true,"internalType":"address",' \
              '"name":"memberAddr","type":"address"},{"indexed":true,"internalType":"uint256","name":"entryId",' \
              '"type":"uint256"},{"indexed":true,"internalType":"address","name":"referrerAddr","type":"address"}],' \
              '"name":"XfLobbyExit","type":"event"},{"payable":true,"stateMutability":"payable","type":"fallback"},' \
              '{"constant":true,"inputs":[],"name":"allocatedSupply","outputs":[{"internalType":"uint256","name":"",' \
              '"type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,' \
              '"inputs":[{"internalType":"address","name":"owner","type":"address"},{"internalType":"address",' \
              '"name":"spender","type":"address"}],"name":"allowance","outputs":[{"internalType":"uint256","name":"",' \
              '"type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,' \
              '"inputs":[{"internalType":"address","name":"spender","type":"address"},{"internalType":"uint256",' \
              '"name":"amount","type":"uint256"}],"name":"approve","outputs":[{"internalType":"bool","name":"",' \
              '"type":"bool"}],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,' \
              '"inputs":[{"internalType":"address","name":"account","type":"address"}],"name":"balanceOf","outputs":[' \
              '{"internalType":"uint256","name":"","type":"uint256"}],"payable":false,"stateMutability":"view",' \
              '"type":"function"},{"constant":false,"inputs":[{"internalType":"uint256","name":"rawSatoshis",' \
              '"type":"uint256"},{"internalType":"bytes32[]","name":"proof","type":"bytes32[]"},' \
              '{"internalType":"address","name":"claimToAddr","type":"address"},{"internalType":"bytes32",' \
              '"name":"pubKeyX","type":"bytes32"},{"internalType":"bytes32","name":"pubKeyY","type":"bytes32"},' \
              '{"internalType":"uint8","name":"claimFlags","type":"uint8"},{"internalType":"uint8","name":"v",' \
              '"type":"uint8"},{"internalType":"bytes32","name":"r","type":"bytes32"},{"internalType":"bytes32",' \
              '"name":"s","type":"bytes32"},{"internalType":"uint256","name":"autoStakeDays","type":"uint256"},' \
              '{"internalType":"address","name":"referrerAddr","type":"address"}],"name":"btcAddressClaim",' \
              '"outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"payable":false,' \
              '"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[{' \
              '"internalType":"bytes20","name":"","type":"bytes20"}],"name":"btcAddressClaims","outputs":[{' \
              '"internalType":"bool","name":"","type":"bool"}],"payable":false,"stateMutability":"view",' \
              '"type":"function"},{"constant":true,"inputs":[{"internalType":"bytes20","name":"btcAddr",' \
              '"type":"bytes20"},{"internalType":"uint256","name":"rawSatoshis","type":"uint256"},' \
              '{"internalType":"bytes32[]","name":"proof","type":"bytes32[]"}],"name":"btcAddressIsClaimable",' \
              '"outputs":[{"internalType":"bool","name":"","type":"bool"}],"payable":false,"stateMutability":"view",' \
              '"type":"function"},{"constant":true,"inputs":[{"internalType":"bytes20","name":"btcAddr",' \
              '"type":"bytes20"},{"internalType":"uint256","name":"rawSatoshis","type":"uint256"},' \
              '{"internalType":"bytes32[]","name":"proof","type":"bytes32[]"}],"name":"btcAddressIsValid","outputs":[' \
              '{"internalType":"bool","name":"","type":"bool"}],"payable":false,"stateMutability":"pure",' \
              '"type":"function"},{"constant":true,"inputs":[{"internalType":"address","name":"claimToAddr",' \
              '"type":"address"},{"internalType":"bytes32","name":"claimParamHash","type":"bytes32"},' \
              '{"internalType":"bytes32","name":"pubKeyX","type":"bytes32"},{"internalType":"bytes32",' \
              '"name":"pubKeyY","type":"bytes32"},{"internalType":"uint8","name":"claimFlags","type":"uint8"},' \
              '{"internalType":"uint8","name":"v","type":"uint8"},{"internalType":"bytes32","name":"r",' \
              '"type":"bytes32"},{"internalType":"bytes32","name":"s","type":"bytes32"}],' \
              '"name":"claimMessageMatchesSignature","outputs":[{"internalType":"bool","name":"","type":"bool"}],' \
              '"payable":false,"stateMutability":"pure","type":"function"},{"constant":true,"inputs":[],' \
              '"name":"currentDay","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"payable":false,' \
              '"stateMutability":"view","type":"function"},{"constant":true,"inputs":[{"internalType":"uint256",' \
              '"name":"","type":"uint256"}],"name":"dailyData","outputs":[{"internalType":"uint72",' \
              '"name":"dayPayoutTotal","type":"uint72"},{"internalType":"uint72","name":"dayStakeSharesTotal",' \
              '"type":"uint72"},{"internalType":"uint56","name":"dayUnclaimedSatoshisTotal","type":"uint56"}],' \
              '"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[{' \
              '"internalType":"uint256","name":"beginDay","type":"uint256"},{"internalType":"uint256",' \
              '"name":"endDay","type":"uint256"}],"name":"dailyDataRange","outputs":[{"internalType":"uint256[]",' \
              '"name":"list","type":"uint256[]"}],"payable":false,"stateMutability":"view","type":"function"},' \
              '{"constant":false,"inputs":[{"internalType":"uint256","name":"beforeDay","type":"uint256"}],' \
              '"name":"dailyDataUpdate","outputs":[],"payable":false,"stateMutability":"nonpayable",' \
              '"type":"function"},{"constant":true,"inputs":[],"name":"decimals","outputs":[{"internalType":"uint8",' \
              '"name":"","type":"uint8"}],"payable":false,"stateMutability":"view","type":"function"},' \
              '{"constant":false,"inputs":[{"internalType":"address","name":"spender","type":"address"},' \
              '{"internalType":"uint256","name":"subtractedValue","type":"uint256"}],"name":"decreaseAllowance",' \
              '"outputs":[{"internalType":"bool","name":"","type":"bool"}],"payable":false,' \
              '"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[],"name":"globalInfo",' \
              '"outputs":[{"internalType":"uint256[13]","name":"","type":"uint256[13]"}],"payable":false,' \
              '"stateMutability":"view","type":"function"},{"constant":true,"inputs":[],"name":"globals","outputs":[{' \
              '"internalType":"uint72","name":"lockedHeartsTotal","type":"uint72"},{"internalType":"uint72",' \
              '"name":"nextStakeSharesTotal","type":"uint72"},{"internalType":"uint40","name":"shareRate",' \
              '"type":"uint40"},{"internalType":"uint72","name":"stakePenaltyTotal","type":"uint72"},' \
              '{"internalType":"uint16","name":"dailyDataCount","type":"uint16"},{"internalType":"uint72",' \
              '"name":"stakeSharesTotal","type":"uint72"},{"internalType":"uint40","name":"latestStakeId",' \
              '"type":"uint40"},{"internalType":"uint128","name":"claimStats","type":"uint128"}],"payable":false,' \
              '"stateMutability":"view","type":"function"},{"constant":false,"inputs":[{"internalType":"address",' \
              '"name":"spender","type":"address"},{"internalType":"uint256","name":"addedValue","type":"uint256"}],' \
              '"name":"increaseAllowance","outputs":[{"internalType":"bool","name":"","type":"bool"}],' \
              '"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[{' \
              '"internalType":"bytes32","name":"merkleLeaf","type":"bytes32"},{"internalType":"bytes32[]",' \
              '"name":"proof","type":"bytes32[]"}],"name":"merkleProofIsValid","outputs":[{"internalType":"bool",' \
              '"name":"","type":"bool"}],"payable":false,"stateMutability":"pure","type":"function"},' \
              '{"constant":true,"inputs":[],"name":"name","outputs":[{"internalType":"string","name":"",' \
              '"type":"string"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,' \
              '"inputs":[{"internalType":"bytes32","name":"pubKeyX","type":"bytes32"},{"internalType":"bytes32",' \
              '"name":"pubKeyY","type":"bytes32"},{"internalType":"uint8","name":"claimFlags","type":"uint8"}],' \
              '"name":"pubKeyToBtcAddress","outputs":[{"internalType":"bytes20","name":"","type":"bytes20"}],' \
              '"payable":false,"stateMutability":"pure","type":"function"},{"constant":true,"inputs":[{' \
              '"internalType":"bytes32","name":"pubKeyX","type":"bytes32"},{"internalType":"bytes32",' \
              '"name":"pubKeyY","type":"bytes32"}],"name":"pubKeyToEthAddress","outputs":[{"internalType":"address",' \
              '"name":"","type":"address"}],"payable":false,"stateMutability":"pure","type":"function"},' \
              '{"constant":true,"inputs":[{"internalType":"address","name":"stakerAddr","type":"address"}],' \
              '"name":"stakeCount","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"payable":false,' \
              '"stateMutability":"view","type":"function"},{"constant":false,"inputs":[{"internalType":"uint256",' \
              '"name":"stakeIndex","type":"uint256"},{"internalType":"uint40","name":"stakeIdParam",' \
              '"type":"uint40"}],"name":"stakeEnd","outputs":[],"payable":false,"stateMutability":"nonpayable",' \
              '"type":"function"},{"constant":false,"inputs":[{"internalType":"address","name":"stakerAddr",' \
              '"type":"address"},{"internalType":"uint256","name":"stakeIndex","type":"uint256"},' \
              '{"internalType":"uint40","name":"stakeIdParam","type":"uint40"}],"name":"stakeGoodAccounting",' \
              '"outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,' \
              '"inputs":[{"internalType":"address","name":"","type":"address"},{"internalType":"uint256","name":"",' \
              '"type":"uint256"}],"name":"stakeLists","outputs":[{"internalType":"uint40","name":"stakeId",' \
              '"type":"uint40"},{"internalType":"uint72","name":"stakedHearts","type":"uint72"},' \
              '{"internalType":"uint72","name":"stakeShares","type":"uint72"},{"internalType":"uint16",' \
              '"name":"lockedDay","type":"uint16"},{"internalType":"uint16","name":"stakedDays","type":"uint16"},' \
              '{"internalType":"uint16","name":"unlockedDay","type":"uint16"},{"internalType":"bool",' \
              '"name":"isAutoStake","type":"bool"}],"payable":false,"stateMutability":"view","type":"function"},' \
              '{"constant":false,"inputs":[{"internalType":"uint256","name":"newStakedHearts","type":"uint256"},' \
              '{"internalType":"uint256","name":"newStakedDays","type":"uint256"}],"name":"stakeStart","outputs":[],' \
              '"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[],' \
              '"name":"symbol","outputs":[{"internalType":"string","name":"","type":"string"}],"payable":false,' \
              '"stateMutability":"view","type":"function"},{"constant":true,"inputs":[],"name":"totalSupply",' \
              '"outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"payable":false,' \
              '"stateMutability":"view","type":"function"},{"constant":false,"inputs":[{"internalType":"address",' \
              '"name":"recipient","type":"address"},{"internalType":"uint256","name":"amount","type":"uint256"}],' \
              '"name":"transfer","outputs":[{"internalType":"bool","name":"","type":"bool"}],"payable":false,' \
              '"stateMutability":"nonpayable","type":"function"},{"constant":false,"inputs":[{' \
              '"internalType":"address","name":"sender","type":"address"},{"internalType":"address",' \
              '"name":"recipient","type":"address"},{"internalType":"uint256","name":"amount","type":"uint256"}],' \
              '"name":"transferFrom","outputs":[{"internalType":"bool","name":"","type":"bool"}],"payable":false,' \
              '"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[{' \
              '"internalType":"uint256","name":"","type":"uint256"}],"name":"xfLobby","outputs":[{' \
              '"internalType":"uint256","name":"","type":"uint256"}],"payable":false,"stateMutability":"view",' \
              '"type":"function"},{"constant":false,"inputs":[{"internalType":"address","name":"referrerAddr",' \
              '"type":"address"}],"name":"xfLobbyEnter","outputs":[],"payable":true,"stateMutability":"payable",' \
              '"type":"function"},{"constant":true,"inputs":[{"internalType":"address","name":"memberAddr",' \
              '"type":"address"},{"internalType":"uint256","name":"entryId","type":"uint256"}],"name":"xfLobbyEntry",' \
              '"outputs":[{"internalType":"uint256","name":"rawAmount","type":"uint256"},{"internalType":"address",' \
              '"name":"referrerAddr","type":"address"}],"payable":false,"stateMutability":"view","type":"function"},' \
              '{"constant":false,"inputs":[{"internalType":"uint256","name":"enterDay","type":"uint256"},' \
              '{"internalType":"uint256","name":"count","type":"uint256"}],"name":"xfLobbyExit","outputs":[],' \
              '"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":false,"inputs":[],' \
              '"name":"xfLobbyFlush","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},' \
              '{"constant":true,"inputs":[{"internalType":"uint256","name":"","type":"uint256"},' \
              '{"internalType":"address","name":"","type":"address"}],"name":"xfLobbyMembers","outputs":[{' \
              '"internalType":"uint40","name":"headIndex","type":"uint40"},{"internalType":"uint40",' \
              '"name":"tailIndex","type":"uint40"}],"payable":false,"stateMutability":"view","type":"function"},' \
              '{"constant":true,"inputs":[{"internalType":"address","name":"memberAddr","type":"address"}],' \
              '"name":"xfLobbyPendingDays","outputs":[{"internalType":"uint256[2]","name":"words","type":"uint256[' \
              '2]"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[{' \
              '"internalType":"uint256","name":"beginDay","type":"uint256"},{"internalType":"uint256",' \
              '"name":"endDay","type":"uint256"}],"name":"xfLobbyRange","outputs":[{"internalType":"uint256[]",' \
              '"name":"list","type":"uint256[]"}],"payable":false,"stateMutability":"view","type":"function"}] ',
    address='0x2b591e99afE9f32eAA6214f7B7629768c40Eeb39',
    deployed_block_height=9041184  # todo change block_height
)


hedron_contract_dict = dict(
    name='hedron',
    abi='[{"inputs":[{"internalType":"address","name":"hexAddress","type":"address"},{"internalType":"uint256",'
        '"name":"hexLaunch","type":"uint256"}],"stateMutability":"nonpayable","type":"constructor"},'
        '{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"owner","type":"address"},'
        '{"indexed":true,"internalType":"address","name":"spender","type":"address"},{"indexed":false,'
        '"internalType":"uint256","name":"value","type":"uint256"}],"name":"Approval","type":"event"},'
        '{"anonymous":false,"inputs":[{"indexed":false,"internalType":"uint256","name":"data","type":"uint256"},'
        '{"indexed":true,"internalType":"address","name":"claimant","type":"address"},{"indexed":true,'
        '"internalType":"uint40","name":"stakeId","type":"uint40"}],"name":"Claim","type":"event"},'
        '{"anonymous":false,"inputs":[{"indexed":false,"internalType":"uint256","name":"data","type":"uint256"},'
        '{"indexed":true,"internalType":"address","name":"borrower","type":"address"},{"indexed":true,'
        '"internalType":"uint40","name":"stakeId","type":"uint40"}],"name":"LoanEnd","type":"event"},'
        '{"anonymous":false,"inputs":[{"indexed":false,"internalType":"uint256","name":"data","type":"uint256"},'
        '{"indexed":true,"internalType":"address","name":"bidder","type":"address"},{"indexed":true,'
        '"internalType":"uint40","name":"stakeId","type":"uint40"},{"indexed":true,"internalType":"uint40",'
        '"name":"liquidationId","type":"uint40"}],"name":"LoanLiquidateBid","type":"event"},{"anonymous":false,'
        '"inputs":[{"indexed":false,"internalType":"uint256","name":"data","type":"uint256"},{"indexed":true,'
        '"internalType":"address","name":"liquidator","type":"address"},{"indexed":true,"internalType":"uint40",'
        '"name":"stakeId","type":"uint40"},{"indexed":true,"internalType":"uint40","name":"liquidationId",'
        '"type":"uint40"}],"name":"LoanLiquidateExit","type":"event"},{"anonymous":false,"inputs":[{"indexed":false,'
        '"internalType":"uint256","name":"data","type":"uint256"},{"indexed":true,"internalType":"address",'
        '"name":"borrower","type":"address"},{"indexed":true,"internalType":"uint40","name":"stakeId",'
        '"type":"uint40"},{"indexed":true,"internalType":"uint40","name":"liquidationId","type":"uint40"}],'
        '"name":"LoanLiquidateStart","type":"event"},{"anonymous":false,"inputs":[{"indexed":false,'
        '"internalType":"uint256","name":"data","type":"uint256"},{"indexed":true,"internalType":"address",'
        '"name":"borrower","type":"address"},{"indexed":true,"internalType":"uint40","name":"stakeId",'
        '"type":"uint40"}],"name":"LoanPayment","type":"event"},{"anonymous":false,"inputs":[{"indexed":false,'
        '"internalType":"uint256","name":"data","type":"uint256"},{"indexed":true,"internalType":"address",'
        '"name":"borrower","type":"address"},{"indexed":true,"internalType":"uint40","name":"stakeId",'
        '"type":"uint40"}],"name":"LoanStart","type":"event"},{"anonymous":false,"inputs":[{"indexed":false,'
        '"internalType":"uint256","name":"data","type":"uint256"},{"indexed":true,"internalType":"address",'
        '"name":"minter","type":"address"},{"indexed":true,"internalType":"uint40","name":"stakeId",'
        '"type":"uint40"}],"name":"Mint","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,'
        '"internalType":"address","name":"from","type":"address"},{"indexed":true,"internalType":"address",'
        '"name":"to","type":"address"},{"indexed":false,"internalType":"uint256","name":"value","type":"uint256"}],'
        '"name":"Transfer","type":"event"},{"inputs":[{"internalType":"address","name":"owner","type":"address"},'
        '{"internalType":"address","name":"spender","type":"address"}],"name":"allowance","outputs":[{'
        '"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},'
        '{"inputs":[{"internalType":"address","name":"spender","type":"address"},{"internalType":"uint256",'
        '"name":"amount","type":"uint256"}],"name":"approve","outputs":[{"internalType":"bool","name":"",'
        '"type":"bool"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address",'
        '"name":"account","type":"address"}],"name":"balanceOf","outputs":[{"internalType":"uint256","name":"",'
        '"type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address",'
        '"name":"borrower","type":"address"},{"internalType":"uint256","name":"hsiIndex","type":"uint256"},'
        '{"internalType":"address","name":"hsiAddress","type":"address"}],"name":"calcLoanPayment","outputs":[{'
        '"internalType":"uint256","name":"","type":"uint256"},{"internalType":"uint256","name":"","type":"uint256"}],'
        '"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"borrower",'
        '"type":"address"},{"internalType":"uint256","name":"hsiIndex","type":"uint256"},{"internalType":"address",'
        '"name":"hsiAddress","type":"address"}],"name":"calcLoanPayoff","outputs":[{"internalType":"uint256",'
        '"name":"","type":"uint256"},{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view",'
        '"type":"function"},{"inputs":[{"internalType":"uint256","name":"hsiIndex","type":"uint256"},'
        '{"internalType":"address","name":"hsiAddress","type":"address"},{"internalType":"address",'
        '"name":"hsiStarterAddress","type":"address"}],"name":"claimInstanced","outputs":[],'
        '"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"stakeIndex",'
        '"type":"uint256"},{"internalType":"uint40","name":"stakeId","type":"uint40"}],"name":"claimNative",'
        '"outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"nonpayable",'
        '"type":"function"},{"inputs":[],"name":"currentDay","outputs":[{"internalType":"uint256","name":"",'
        '"type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256",'
        '"name":"","type":"uint256"}],"name":"dailyDataList","outputs":[{"internalType":"uint72",'
        '"name":"dayMintedTotal","type":"uint72"},{"internalType":"uint72","name":"dayLoanedTotal","type":"uint72"},'
        '{"internalType":"uint72","name":"dayBurntTotal","type":"uint72"},{"internalType":"uint32",'
        '"name":"dayInterestRate","type":"uint32"},{"internalType":"uint8","name":"dayMintMultiplier",'
        '"type":"uint8"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"decimals","outputs":[{'
        '"internalType":"uint8","name":"","type":"uint8"}],"stateMutability":"view","type":"function"},{"inputs":[{'
        '"internalType":"address","name":"spender","type":"address"},{"internalType":"uint256",'
        '"name":"subtractedValue","type":"uint256"}],"name":"decreaseAllowance","outputs":[{"internalType":"bool",'
        '"name":"","type":"bool"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"hsim",'
        '"outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view",'
        '"type":"function"},{"inputs":[{"internalType":"address","name":"spender","type":"address"},'
        '{"internalType":"uint256","name":"addedValue","type":"uint256"}],"name":"increaseAllowance","outputs":[{'
        '"internalType":"bool","name":"","type":"bool"}],"stateMutability":"nonpayable","type":"function"},'
        '{"inputs":[{"internalType":"uint256","name":"","type":"uint256"}],"name":"liquidationList","outputs":[{'
        '"internalType":"uint256","name":"liquidationStart","type":"uint256"},{"internalType":"address",'
        '"name":"hsiAddress","type":"address"},{"internalType":"uint96","name":"bidAmount","type":"uint96"},'
        '{"internalType":"address","name":"liquidator","type":"address"},{"internalType":"uint88","name":"endOffset",'
        '"type":"uint88"},{"internalType":"bool","name":"isActive","type":"bool"}],"stateMutability":"view",'
        '"type":"function"},{"inputs":[{"internalType":"uint256","name":"hsiIndex","type":"uint256"},'
        '{"internalType":"address","name":"hsiAddress","type":"address"}],"name":"loanInstanced","outputs":[{'
        '"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"nonpayable","type":"function"},'
        '{"inputs":[{"internalType":"address","name":"owner","type":"address"},{"internalType":"uint256",'
        '"name":"hsiIndex","type":"uint256"},{"internalType":"address","name":"hsiAddress","type":"address"}],'
        '"name":"loanLiquidate","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],'
        '"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256",'
        '"name":"liquidationId","type":"uint256"},{"internalType":"uint256","name":"liquidationBid",'
        '"type":"uint256"}],"name":"loanLiquidateBid","outputs":[{"internalType":"uint256","name":"",'
        '"type":"uint256"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256",'
        '"name":"hsiIndex","type":"uint256"},{"internalType":"uint256","name":"liquidationId","type":"uint256"}],'
        '"name":"loanLiquidateExit","outputs":[{"internalType":"address","name":"","type":"address"}],'
        '"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"hsiIndex",'
        '"type":"uint256"},{"internalType":"address","name":"hsiAddress","type":"address"}],"name":"loanPayment",'
        '"outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"nonpayable",'
        '"type":"function"},{"inputs":[{"internalType":"uint256","name":"hsiIndex","type":"uint256"},'
        '{"internalType":"address","name":"hsiAddress","type":"address"}],"name":"loanPayoff","outputs":[{'
        '"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"nonpayable","type":"function"},'
        '{"inputs":[],"name":"loanedSupply","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],'
        '"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256","name":"hsiIndex",'
        '"type":"uint256"},{"internalType":"address","name":"hsiAddress","type":"address"}],"name":"mintInstanced",'
        '"outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"nonpayable",'
        '"type":"function"},{"inputs":[{"internalType":"uint256","name":"stakeIndex","type":"uint256"},'
        '{"internalType":"uint40","name":"stakeId","type":"uint40"}],"name":"mintNative","outputs":[{'
        '"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"nonpayable","type":"function"},'
        '{"inputs":[],"name":"name","outputs":[{"internalType":"string","name":"","type":"string"}],'
        '"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256","name":"amount",'
        '"type":"uint256"}],"name":"proofOfBenevolence","outputs":[],"stateMutability":"nonpayable",'
        '"type":"function"},{"inputs":[{"internalType":"uint256","name":"","type":"uint256"}],"name":"shareList",'
        '"outputs":[{"components":[{"internalType":"uint40","name":"stakeId","type":"uint40"},'
        '{"internalType":"uint72","name":"stakeShares","type":"uint72"},{"internalType":"uint16","name":"lockedDay",'
        '"type":"uint16"},{"internalType":"uint16","name":"stakedDays","type":"uint16"}],"internalType":"struct '
        'HEXStakeMinimal","name":"stake","type":"tuple"},{"internalType":"uint16","name":"mintedDays",'
        '"type":"uint16"},{"internalType":"uint8","name":"launchBonus","type":"uint8"},{"internalType":"uint16",'
        '"name":"loanStart","type":"uint16"},{"internalType":"uint16","name":"loanedDays","type":"uint16"},'
        '{"internalType":"uint32","name":"interestRate","type":"uint32"},{"internalType":"uint8",'
        '"name":"paymentsMade","type":"uint8"},{"internalType":"bool","name":"isLoaned","type":"bool"}],'
        '"stateMutability":"view","type":"function"},{"inputs":[],"name":"symbol","outputs":[{'
        '"internalType":"string","name":"","type":"string"}],"stateMutability":"view","type":"function"},{"inputs":['
        '],"name":"totalSupply","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],'
        '"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"recipient",'
        '"type":"address"},{"internalType":"uint256","name":"amount","type":"uint256"}],"name":"transfer","outputs":['
        '{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"nonpayable","type":"function"},'
        '{"inputs":[{"internalType":"address","name":"sender","type":"address"},{"internalType":"address",'
        '"name":"recipient","type":"address"},{"internalType":"uint256","name":"amount","type":"uint256"}],'
        '"name":"transferFrom","outputs":[{"internalType":"bool","name":"","type":"bool"}],'
        '"stateMutability":"nonpayable","type":"function"}]',
    address='0x3819f64f282bf135d62168C1e513280dAF905e06',
    deployed_block_height=14240942
)


hex_stake_instance_dict = dict(
    name='hex_stake_instance',
    abi='[{"inputs":[{"internalType":"address","name":"hexAddress","type":"address"}],"stateMutability":"nonpayable",'
        '"type":"constructor"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"owner",'
        '"type":"address"},{"indexed":true,"internalType":"address","name":"approved","type":"address"},'
        '{"indexed":true,"internalType":"uint256","name":"tokenId","type":"uint256"}],"name":"Approval",'
        '"type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"owner",'
        '"type":"address"},{"indexed":true,"internalType":"address","name":"operator","type":"address"},'
        '{"indexed":false,"internalType":"bool","name":"approved","type":"bool"}],"name":"ApprovalForAll",'
        '"type":"event"},{"anonymous":false,"inputs":[{"indexed":false,"internalType":"uint256","name":"timestamp",'
        '"type":"uint256"},{"indexed":true,"internalType":"uint256","name":"hsiTokenId","type":"uint256"},'
        '{"indexed":true,"internalType":"address","name":"hsiAddress","type":"address"},{"indexed":true,'
        '"internalType":"address","name":"staker","type":"address"}],"name":"HSIDetokenize","type":"event"},'
        '{"anonymous":false,"inputs":[{"indexed":false,"internalType":"uint256","name":"timestamp","type":"uint256"},'
        '{"indexed":true,"internalType":"address","name":"hsiAddress","type":"address"},{"indexed":true,'
        '"internalType":"address","name":"staker","type":"address"}],"name":"HSIEnd","type":"event"},'
        '{"anonymous":false,"inputs":[{"indexed":false,"internalType":"uint256","name":"timestamp","type":"uint256"},'
        '{"indexed":true,"internalType":"address","name":"hsiAddress","type":"address"},{"indexed":true,'
        '"internalType":"address","name":"staker","type":"address"}],"name":"HSIStart","type":"event"},'
        '{"anonymous":false,"inputs":[{"indexed":false,"internalType":"uint256","name":"timestamp","type":"uint256"},'
        '{"indexed":true,"internalType":"uint256","name":"hsiTokenId","type":"uint256"},{"indexed":true,'
        '"internalType":"address","name":"hsiAddress","type":"address"},{"indexed":true,"internalType":"address",'
        '"name":"staker","type":"address"}],"name":"HSITokenize","type":"event"},{"anonymous":false,"inputs":[{'
        '"indexed":false,"internalType":"uint256","name":"timestamp","type":"uint256"},{"indexed":true,'
        '"internalType":"address","name":"hsiAddress","type":"address"},{"indexed":true,"internalType":"address",'
        '"name":"oldStaker","type":"address"},{"indexed":true,"internalType":"address","name":"newStaker",'
        '"type":"address"}],"name":"HSITransfer","type":"event"},{"anonymous":false,"inputs":[{"indexed":false,'
        '"internalType":"uint256","name":"tokenId","type":"uint256"},{"components":[{"internalType":"address '
        'payable","name":"account","type":"address"},{"internalType":"uint96","name":"value","type":"uint96"}],'
        '"indexed":false,"internalType":"struct LibPart.Part[]","name":"royalties","type":"tuple[]"}],'
        '"name":"RoyaltiesSet","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address",'
        '"name":"from","type":"address"},{"indexed":true,"internalType":"address","name":"to","type":"address"},'
        '{"indexed":true,"internalType":"uint256","name":"tokenId","type":"uint256"}],"name":"Transfer",'
        '"type":"event"},{"inputs":[{"internalType":"address","name":"to","type":"address"},'
        '{"internalType":"uint256","name":"tokenId","type":"uint256"}],"name":"approve","outputs":[],'
        '"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"owner",'
        '"type":"address"}],"name":"balanceOf","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],'
        '"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256","name":"tokenId",'
        '"type":"uint256"}],"name":"getApproved","outputs":[{"internalType":"address","name":"","type":"address"}],'
        '"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256","name":"id",'
        '"type":"uint256"}],"name":"getRaribleV2Royalties","outputs":[{"components":[{"internalType":"address '
        'payable","name":"account","type":"address"},{"internalType":"uint96","name":"value","type":"uint96"}],'
        '"internalType":"struct LibPart.Part[]","name":"","type":"tuple[]"}],"stateMutability":"view",'
        '"type":"function"},{"inputs":[{"internalType":"uint256","name":"tokenId","type":"uint256"}],'
        '"name":"hexStakeDetokenize","outputs":[{"internalType":"address","name":"","type":"address"}],'
        '"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"hsiIndex",'
        '"type":"uint256"},{"internalType":"address","name":"hsiAddress","type":"address"}],"name":"hexStakeEnd",'
        '"outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"nonpayable",'
        '"type":"function"},{"inputs":[{"internalType":"uint256","name":"amount","type":"uint256"},'
        '{"internalType":"uint256","name":"length","type":"uint256"}],"name":"hexStakeStart","outputs":[{'
        '"internalType":"address","name":"","type":"address"}],"stateMutability":"nonpayable","type":"function"},'
        '{"inputs":[{"internalType":"uint256","name":"hsiIndex","type":"uint256"},{"internalType":"address",'
        '"name":"hsiAddress","type":"address"}],"name":"hexStakeTokenize","outputs":[{"internalType":"uint256",'
        '"name":"","type":"uint256"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{'
        '"internalType":"address","name":"user","type":"address"}],"name":"hsiCount","outputs":[{'
        '"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},'
        '{"inputs":[{"internalType":"address","name":"","type":"address"},{"internalType":"uint256","name":"",'
        '"type":"uint256"}],"name":"hsiLists","outputs":[{"internalType":"address","name":"","type":"address"}],'
        '"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256","name":"",'
        '"type":"uint256"}],"name":"hsiToken","outputs":[{"internalType":"address","name":"","type":"address"}],'
        '"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"currentHolder",'
        '"type":"address"},{"internalType":"uint256","name":"hsiIndex","type":"uint256"},{"internalType":"address",'
        '"name":"hsiAddress","type":"address"},{"internalType":"address","name":"newHolder","type":"address"}],'
        '"name":"hsiTransfer","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{'
        '"internalType":"address","name":"holder","type":"address"},{"internalType":"uint256","name":"hsiIndex",'
        '"type":"uint256"},{"internalType":"address","name":"hsiAddress","type":"address"},{"components":[{'
        '"components":[{"internalType":"uint40","name":"stakeId","type":"uint40"},{"internalType":"uint72",'
        '"name":"stakeShares","type":"uint72"},{"internalType":"uint16","name":"lockedDay","type":"uint16"},'
        '{"internalType":"uint16","name":"stakedDays","type":"uint16"}],"internalType":"struct HEXStakeMinimal",'
        '"name":"_stake","type":"tuple"},{"internalType":"uint256","name":"_mintedDays","type":"uint256"},'
        '{"internalType":"uint256","name":"_launchBonus","type":"uint256"},{"internalType":"uint256",'
        '"name":"_loanStart","type":"uint256"},{"internalType":"uint256","name":"_loanedDays","type":"uint256"},'
        '{"internalType":"uint256","name":"_interestRate","type":"uint256"},{"internalType":"uint256",'
        '"name":"_paymentsMade","type":"uint256"},{"internalType":"bool","name":"_isLoaned","type":"bool"}],'
        '"internalType":"struct ShareCache","name":"share","type":"tuple"}],"name":"hsiUpdate","outputs":[],'
        '"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"owner",'
        '"type":"address"},{"internalType":"address","name":"operator","type":"address"}],"name":"isApprovedForAll",'
        '"outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"view","type":"function"},'
        '{"inputs":[],"name":"name","outputs":[{"internalType":"string","name":"","type":"string"}],'
        '"stateMutability":"view","type":"function"},{"inputs":[],"name":"owner","outputs":[{'
        '"internalType":"address","name":"","type":"address"}],"stateMutability":"pure","type":"function"},'
        '{"inputs":[{"internalType":"uint256","name":"tokenId","type":"uint256"}],"name":"ownerOf","outputs":[{'
        '"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},'
        '{"inputs":[{"internalType":"uint256","name":"tokenId","type":"uint256"},{"internalType":"uint256",'
        '"name":"salePrice","type":"uint256"}],"name":"royaltyInfo","outputs":[{"internalType":"address",'
        '"name":"receiver","type":"address"},{"internalType":"uint256","name":"royaltyAmount","type":"uint256"}],'
        '"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"from",'
        '"type":"address"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256",'
        '"name":"tokenId","type":"uint256"}],"name":"safeTransferFrom","outputs":[],"stateMutability":"nonpayable",'
        '"type":"function"},{"inputs":[{"internalType":"address","name":"from","type":"address"},'
        '{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"tokenId",'
        '"type":"uint256"},{"internalType":"bytes","name":"_data","type":"bytes"}],"name":"safeTransferFrom",'
        '"outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address",'
        '"name":"operator","type":"address"},{"internalType":"bool","name":"approved","type":"bool"}],'
        '"name":"setApprovalForAll","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{'
        '"internalType":"address","name":"user","type":"address"}],"name":"stakeCount","outputs":[{'
        '"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},'
        '{"inputs":[{"internalType":"address","name":"user","type":"address"},{"internalType":"uint256",'
        '"name":"hsiIndex","type":"uint256"}],"name":"stakeLists","outputs":[{"components":[{"internalType":"uint40",'
        '"name":"stakeId","type":"uint40"},{"internalType":"uint72","name":"stakedHearts","type":"uint72"},'
        '{"internalType":"uint72","name":"stakeShares","type":"uint72"},{"internalType":"uint16","name":"lockedDay",'
        '"type":"uint16"},{"internalType":"uint16","name":"stakedDays","type":"uint16"},{"internalType":"uint16",'
        '"name":"unlockedDay","type":"uint16"},{"internalType":"bool","name":"isAutoStake","type":"bool"}],'
        '"internalType":"struct HEXStake","name":"","type":"tuple"}],"stateMutability":"view","type":"function"},'
        '{"inputs":[{"internalType":"bytes4","name":"interfaceId","type":"bytes4"}],"name":"supportsInterface",'
        '"outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"view","type":"function"},'
        '{"inputs":[],"name":"symbol","outputs":[{"internalType":"string","name":"","type":"string"}],'
        '"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256","name":"index",'
        '"type":"uint256"}],"name":"tokenByIndex","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],'
        '"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"owner",'
        '"type":"address"},{"internalType":"uint256","name":"index","type":"uint256"}],"name":"tokenOfOwnerByIndex",'
        '"outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view",'
        '"type":"function"},{"inputs":[{"internalType":"uint256","name":"tokenId","type":"uint256"}],'
        '"name":"tokenURI","outputs":[{"internalType":"string","name":"","type":"string"}],"stateMutability":"view",'
        '"type":"function"},{"inputs":[],"name":"totalSupply","outputs":[{"internalType":"uint256","name":"",'
        '"type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address",'
        '"name":"from","type":"address"},{"internalType":"address","name":"to","type":"address"},'
        '{"internalType":"uint256","name":"tokenId","type":"uint256"}],"name":"transferFrom","outputs":[],'
        '"stateMutability":"nonpayable","type":"function"}]',
    address='0x8BD3d1472A656e312E94fB1BbdD599B8C51D18e3',
    deployed_block_height=14240942
)


pulsedogecoin_contract_dict = dict(
    name='pulsedogecoin',
    abi='[{"inputs":[],"stateMutability":"nonpayable","type":"constructor"},{"anonymous":false,"inputs":[{'
        '"indexed":true,"internalType":"address","name":"owner","type":"address"},{"indexed":true,'
        '"internalType":"address","name":"spender","type":"address"},{"indexed":false,"internalType":"uint256",'
        '"name":"value","type":"uint256"}],"name":"Approval","type":"event"},{"anonymous":false,"inputs":[{'
        '"indexed":true,"internalType":"address","name":"to","type":"address"},{"indexed":false,'
        '"internalType":"uint256","name":"amount","type":"uint256"}],"name":"Claim","type":"event"},'
        '{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"from","type":"address"},'
        '{"indexed":true,"internalType":"address","name":"to","type":"address"},{"indexed":false,'
        '"internalType":"uint256","name":"value","type":"uint256"}],"name":"Transfer","type":"event"},{"inputs":[{'
        '"internalType":"address","name":"owner","type":"address"},{"internalType":"address","name":"spender",'
        '"type":"address"}],"name":"allowance","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],'
        '"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"spender",'
        '"type":"address"},{"internalType":"uint256","name":"amount","type":"uint256"}],"name":"approve","outputs":[{'
        '"internalType":"bool","name":"","type":"bool"}],"stateMutability":"nonpayable","type":"function"},'
        '{"inputs":[{"internalType":"address","name":"account","type":"address"}],"name":"balanceOf","outputs":[{'
        '"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},'
        '{"inputs":[{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256",'
        '"name":"amount","type":"uint256"},{"internalType":"bytes32[]","name":"proof","type":"bytes32[]"}],'
        '"name":"claim","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[],'
        '"name":"currentDay","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],'
        '"stateMutability":"view","type":"function"},{"inputs":[],"name":"decimals","outputs":[{'
        '"internalType":"uint8","name":"","type":"uint8"}],"stateMutability":"view","type":"function"},{"inputs":[{'
        '"internalType":"address","name":"spender","type":"address"},{"internalType":"uint256",'
        '"name":"subtractedValue","type":"uint256"}],"name":"decreaseAllowance","outputs":[{"internalType":"bool",'
        '"name":"","type":"bool"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{'
        '"internalType":"address","name":"","type":"address"}],"name":"hasClaimed","outputs":[{"internalType":"bool",'
        '"name":"","type":"bool"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address",'
        '"name":"hexAddr","type":"address"},{"internalType":"uint256","name":"plsdAmount","type":"uint256"},'
        '{"internalType":"bytes32[]","name":"proof","type":"bytes32[]"}],"name":"hexAddressIsClaimable","outputs":[{'
        '"internalType":"bool","name":"","type":"bool"}],"stateMutability":"pure","type":"function"},{"inputs":[{'
        '"internalType":"address","name":"spender","type":"address"},{"internalType":"uint256","name":"addedValue",'
        '"type":"uint256"}],"name":"increaseAllowance","outputs":[{"internalType":"bool","name":"","type":"bool"}],'
        '"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"launchTime","outputs":[{'
        '"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},'
        '{"inputs":[],"name":"mintOaBaTokens","outputs":[],"stateMutability":"nonpayable","type":"function"},'
        '{"inputs":[],"name":"name","outputs":[{"internalType":"string","name":"","type":"string"}],'
        '"stateMutability":"view","type":"function"},{"inputs":[],"name":"numberOfClaims","outputs":[{'
        '"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},'
        '{"inputs":[],"name":"symbol","outputs":[{"internalType":"string","name":"","type":"string"}],'
        '"stateMutability":"view","type":"function"},{"inputs":[],"name":"totalSupply","outputs":[{'
        '"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},'
        '{"inputs":[{"internalType":"address","name":"recipient","type":"address"},{"internalType":"uint256",'
        '"name":"amount","type":"uint256"}],"name":"transfer","outputs":[{"internalType":"bool","name":"",'
        '"type":"bool"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address",'
        '"name":"sender","type":"address"},{"internalType":"address","name":"recipient","type":"address"},'
        '{"internalType":"uint256","name":"amount","type":"uint256"}],"name":"transferFrom","outputs":[{'
        '"internalType":"bool","name":"","type":"bool"}],"stateMutability":"nonpayable","type":"function"}]',
    address='0x34F0915a5f15a66Eba86F6a58bE1A471FB7836A7',
    deployed_block_height=14622411
)


maximus_contract_dict = dict(
    name='maximus',
    abi='[{"inputs":[{"internalType":"uint256","name":"mint_duration","type":"uint256"},{"internalType":"uint256",'
        '"name":"stake_duration","type":"uint256"}],"stateMutability":"nonpayable","type":"constructor"},'
        '{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"owner","type":"address"},'
        '{"indexed":true,"internalType":"address","name":"spender","type":"address"},{"indexed":false,'
        '"internalType":"uint256","name":"value","type":"uint256"}],"name":"Approval","type":"event"},'
        '{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"from","type":"address"},'
        '{"indexed":true,"internalType":"address","name":"to","type":"address"},{"indexed":false,'
        '"internalType":"uint256","name":"value","type":"uint256"}],"name":"Transfer","type":"event"},{"inputs":[{'
        '"internalType":"address","name":"owner","type":"address"},{"internalType":"address","name":"spender",'
        '"type":"address"}],"name":"allowance","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],'
        '"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"spender",'
        '"type":"address"},{"internalType":"uint256","name":"amount","type":"uint256"}],"name":"approve","outputs":[{'
        '"internalType":"bool","name":"","type":"bool"}],"stateMutability":"nonpayable","type":"function"},'
        '{"inputs":[{"internalType":"address","name":"account","type":"address"}],"name":"balanceOf","outputs":[{'
        '"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},'
        '{"inputs":[{"internalType":"uint256","name":"amount","type":"uint256"}],"name":"burn","outputs":[],'
        '"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"account",'
        '"type":"address"},{"internalType":"uint256","name":"amount","type":"uint256"}],"name":"burnFrom","outputs":['
        '],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"decimals","outputs":[{'
        '"internalType":"uint8","name":"","type":"uint8"}],"stateMutability":"view","type":"function"},{"inputs":[{'
        '"internalType":"address","name":"spender","type":"address"},{"internalType":"uint256",'
        '"name":"subtractedValue","type":"uint256"}],"name":"decreaseAllowance","outputs":[{"internalType":"bool",'
        '"name":"","type":"bool"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{'
        '"internalType":"uint256","name":"stakeIndex","type":"uint256"},{"internalType":"uint40",'
        '"name":"stakeIdParam","type":"uint40"}],"name":"endStakeHEX","outputs":[],"stateMutability":"nonpayable",'
        '"type":"function"},{"inputs":[],"name":"getEndStaker","outputs":[{"internalType":"address",'
        '"name":"end_staker_address","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[],'
        '"name":"getHEXRedemptionRate","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],'
        '"stateMutability":"view","type":"function"},{"inputs":[],"name":"getHedronDay","outputs":[{'
        '"internalType":"uint256","name":"day","type":"uint256"}],"stateMutability":"view","type":"function"},'
        '{"inputs":[],"name":"getHedronRedemptionRate","outputs":[{"internalType":"uint256","name":"",'
        '"type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"getHexDay","outputs":[{'
        '"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},'
        '{"inputs":[],"name":"getMintingPhaseEndDay","outputs":[{"internalType":"uint256","name":"",'
        '"type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],'
        '"name":"getMintingPhaseStartDay","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],'
        '"stateMutability":"view","type":"function"},{"inputs":[],"name":"getStakeEndDay","outputs":[{'
        '"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},'
        '{"inputs":[],"name":"getStakeStartDay","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],'
        '"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"spender",'
        '"type":"address"},{"internalType":"uint256","name":"addedValue","type":"uint256"}],'
        '"name":"increaseAllowance","outputs":[{"internalType":"bool","name":"","type":"bool"}],'
        '"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"stakeIndex",'
        '"type":"uint256"},{"internalType":"uint40","name":"stakeId","type":"uint40"}],"name":"mintHedron",'
        '"outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"name","outputs":[{'
        '"internalType":"string","name":"","type":"string"}],"stateMutability":"view","type":"function"},{"inputs":[{'
        '"internalType":"uint256","name":"amount","type":"uint256"}],"name":"pledgeHEX","outputs":[],'
        '"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"amount_MAXI",'
        '"type":"uint256"}],"name":"redeemHEX","outputs":[],"stateMutability":"nonpayable","type":"function"},'
        '{"inputs":[],"name":"stakeHEX","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[],'
        '"name":"symbol","outputs":[{"internalType":"string","name":"","type":"string"}],"stateMutability":"view",'
        '"type":"function"},{"inputs":[],"name":"totalSupply","outputs":[{"internalType":"uint256","name":"",'
        '"type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address",'
        '"name":"to","type":"address"},{"internalType":"uint256","name":"amount","type":"uint256"}],'
        '"name":"transfer","outputs":[{"internalType":"bool","name":"","type":"bool"}],'
        '"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"from",'
        '"type":"address"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256",'
        '"name":"amount","type":"uint256"}],"name":"transferFrom","outputs":[{"internalType":"bool","name":"",'
        '"type":"bool"}],"stateMutability":"nonpayable","type":"function"}]',
    address='0x0d86EB9f43C57f6FF3BC9E23D8F9d82503f0e84b',
    deployed_block_height=14593069
)


uniswap_v3_positions_config = dict(
    name='uniswap_v3_positions',
    abi='[{"inputs":[{"internalType":"address","name":"_factory","type":"address"},{"internalType":"address",'
        '"name":"_WETH9","type":"address"},{"internalType":"address","name":"_tokenDescriptor_","type":"address"}],'
        '"stateMutability":"nonpayable","type":"constructor"},{"anonymous":false,"inputs":[{"indexed":true,'
        '"internalType":"address","name":"owner","type":"address"},{"indexed":true,"internalType":"address",'
        '"name":"approved","type":"address"},{"indexed":true,"internalType":"uint256","name":"tokenId",'
        '"type":"uint256"}],"name":"Approval","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,'
        '"internalType":"address","name":"owner","type":"address"},{"indexed":true,"internalType":"address",'
        '"name":"operator","type":"address"},{"indexed":false,"internalType":"bool","name":"approved",'
        '"type":"bool"}],"name":"ApprovalForAll","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,'
        '"internalType":"uint256","name":"tokenId","type":"uint256"},{"indexed":false,"internalType":"address",'
        '"name":"recipient","type":"address"},{"indexed":false,"internalType":"uint256","name":"amount0",'
        '"type":"uint256"},{"indexed":false,"internalType":"uint256","name":"amount1","type":"uint256"}],'
        '"name":"Collect","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"uint256",'
        '"name":"tokenId","type":"uint256"},{"indexed":false,"internalType":"uint128","name":"liquidity",'
        '"type":"uint128"},{"indexed":false,"internalType":"uint256","name":"amount0","type":"uint256"},'
        '{"indexed":false,"internalType":"uint256","name":"amount1","type":"uint256"}],"name":"DecreaseLiquidity",'
        '"type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"uint256","name":"tokenId",'
        '"type":"uint256"},{"indexed":false,"internalType":"uint128","name":"liquidity","type":"uint128"},'
        '{"indexed":false,"internalType":"uint256","name":"amount0","type":"uint256"},{"indexed":false,'
        '"internalType":"uint256","name":"amount1","type":"uint256"}],"name":"IncreaseLiquidity","type":"event"},'
        '{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"from","type":"address"},'
        '{"indexed":true,"internalType":"address","name":"to","type":"address"},{"indexed":true,'
        '"internalType":"uint256","name":"tokenId","type":"uint256"}],"name":"Transfer","type":"event"},{"inputs":[],'
        '"name":"DOMAIN_SEPARATOR","outputs":[{"internalType":"bytes32","name":"","type":"bytes32"}],'
        '"stateMutability":"view","type":"function"},{"inputs":[],"name":"PERMIT_TYPEHASH","outputs":[{'
        '"internalType":"bytes32","name":"","type":"bytes32"}],"stateMutability":"view","type":"function"},'
        '{"inputs":[],"name":"WETH9","outputs":[{"internalType":"address","name":"","type":"address"}],'
        '"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"to",'
        '"type":"address"},{"internalType":"uint256","name":"tokenId","type":"uint256"}],"name":"approve","outputs":['
        '],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"owner",'
        '"type":"address"}],"name":"balanceOf","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],'
        '"stateMutability":"view","type":"function"},{"inputs":[],"name":"baseURI","outputs":[{'
        '"internalType":"string","name":"","type":"string"}],"stateMutability":"pure","type":"function"},{"inputs":[{'
        '"internalType":"uint256","name":"tokenId","type":"uint256"}],"name":"burn","outputs":[],'
        '"stateMutability":"payable","type":"function"},{"inputs":[{"components":[{"internalType":"uint256",'
        '"name":"tokenId","type":"uint256"},{"internalType":"address","name":"recipient","type":"address"},'
        '{"internalType":"uint128","name":"amount0Max","type":"uint128"},{"internalType":"uint128",'
        '"name":"amount1Max","type":"uint128"}],"internalType":"struct INonfungiblePositionManager.CollectParams",'
        '"name":"params","type":"tuple"}],"name":"collect","outputs":[{"internalType":"uint256","name":"amount0",'
        '"type":"uint256"},{"internalType":"uint256","name":"amount1","type":"uint256"}],"stateMutability":"payable",'
        '"type":"function"},{"inputs":[{"internalType":"address","name":"token0","type":"address"},'
        '{"internalType":"address","name":"token1","type":"address"},{"internalType":"uint24","name":"fee",'
        '"type":"uint24"},{"internalType":"uint160","name":"sqrtPriceX96","type":"uint160"}],'
        '"name":"createAndInitializePoolIfNecessary","outputs":[{"internalType":"address","name":"pool",'
        '"type":"address"}],"stateMutability":"payable","type":"function"},{"inputs":[{"components":[{'
        '"internalType":"uint256","name":"tokenId","type":"uint256"},{"internalType":"uint128","name":"liquidity",'
        '"type":"uint128"},{"internalType":"uint256","name":"amount0Min","type":"uint256"},{"internalType":"uint256",'
        '"name":"amount1Min","type":"uint256"},{"internalType":"uint256","name":"deadline","type":"uint256"}],'
        '"internalType":"struct INonfungiblePositionManager.DecreaseLiquidityParams","name":"params",'
        '"type":"tuple"}],"name":"decreaseLiquidity","outputs":[{"internalType":"uint256","name":"amount0",'
        '"type":"uint256"},{"internalType":"uint256","name":"amount1","type":"uint256"}],"stateMutability":"payable",'
        '"type":"function"},{"inputs":[],"name":"factory","outputs":[{"internalType":"address","name":"",'
        '"type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256",'
        '"name":"tokenId","type":"uint256"}],"name":"getApproved","outputs":[{"internalType":"address","name":"",'
        '"type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[{"components":[{'
        '"internalType":"uint256","name":"tokenId","type":"uint256"},{"internalType":"uint256",'
        '"name":"amount0Desired","type":"uint256"},{"internalType":"uint256","name":"amount1Desired",'
        '"type":"uint256"},{"internalType":"uint256","name":"amount0Min","type":"uint256"},{"internalType":"uint256",'
        '"name":"amount1Min","type":"uint256"},{"internalType":"uint256","name":"deadline","type":"uint256"}],'
        '"internalType":"struct INonfungiblePositionManager.IncreaseLiquidityParams","name":"params",'
        '"type":"tuple"}],"name":"increaseLiquidity","outputs":[{"internalType":"uint128","name":"liquidity",'
        '"type":"uint128"},{"internalType":"uint256","name":"amount0","type":"uint256"},{"internalType":"uint256",'
        '"name":"amount1","type":"uint256"}],"stateMutability":"payable","type":"function"},{"inputs":[{'
        '"internalType":"address","name":"owner","type":"address"},{"internalType":"address","name":"operator",'
        '"type":"address"}],"name":"isApprovedForAll","outputs":[{"internalType":"bool","name":"","type":"bool"}],'
        '"stateMutability":"view","type":"function"},{"inputs":[{"components":[{"internalType":"address",'
        '"name":"token0","type":"address"},{"internalType":"address","name":"token1","type":"address"},'
        '{"internalType":"uint24","name":"fee","type":"uint24"},{"internalType":"int24","name":"tickLower",'
        '"type":"int24"},{"internalType":"int24","name":"tickUpper","type":"int24"},{"internalType":"uint256",'
        '"name":"amount0Desired","type":"uint256"},{"internalType":"uint256","name":"amount1Desired",'
        '"type":"uint256"},{"internalType":"uint256","name":"amount0Min","type":"uint256"},{"internalType":"uint256",'
        '"name":"amount1Min","type":"uint256"},{"internalType":"address","name":"recipient","type":"address"},'
        '{"internalType":"uint256","name":"deadline","type":"uint256"}],"internalType":"struct '
        'INonfungiblePositionManager.MintParams","name":"params","type":"tuple"}],"name":"mint","outputs":[{'
        '"internalType":"uint256","name":"tokenId","type":"uint256"},{"internalType":"uint128","name":"liquidity",'
        '"type":"uint128"},{"internalType":"uint256","name":"amount0","type":"uint256"},{"internalType":"uint256",'
        '"name":"amount1","type":"uint256"}],"stateMutability":"payable","type":"function"},{"inputs":[{'
        '"internalType":"bytes[]","name":"data","type":"bytes[]"}],"name":"multicall","outputs":[{'
        '"internalType":"bytes[]","name":"results","type":"bytes[]"}],"stateMutability":"payable","type":"function"},'
        '{"inputs":[],"name":"name","outputs":[{"internalType":"string","name":"","type":"string"}],'
        '"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256","name":"tokenId",'
        '"type":"uint256"}],"name":"ownerOf","outputs":[{"internalType":"address","name":"","type":"address"}],'
        '"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"spender",'
        '"type":"address"},{"internalType":"uint256","name":"tokenId","type":"uint256"},{"internalType":"uint256",'
        '"name":"deadline","type":"uint256"},{"internalType":"uint8","name":"v","type":"uint8"},'
        '{"internalType":"bytes32","name":"r","type":"bytes32"},{"internalType":"bytes32","name":"s",'
        '"type":"bytes32"}],"name":"permit","outputs":[],"stateMutability":"payable","type":"function"},{"inputs":[{'
        '"internalType":"uint256","name":"tokenId","type":"uint256"}],"name":"positions","outputs":[{'
        '"internalType":"uint96","name":"nonce","type":"uint96"},{"internalType":"address","name":"operator",'
        '"type":"address"},{"internalType":"address","name":"token0","type":"address"},{"internalType":"address",'
        '"name":"token1","type":"address"},{"internalType":"uint24","name":"fee","type":"uint24"},'
        '{"internalType":"int24","name":"tickLower","type":"int24"},{"internalType":"int24","name":"tickUpper",'
        '"type":"int24"},{"internalType":"uint128","name":"liquidity","type":"uint128"},{"internalType":"uint256",'
        '"name":"feeGrowthInside0LastX128","type":"uint256"},{"internalType":"uint256",'
        '"name":"feeGrowthInside1LastX128","type":"uint256"},{"internalType":"uint128","name":"tokensOwed0",'
        '"type":"uint128"},{"internalType":"uint128","name":"tokensOwed1","type":"uint128"}],'
        '"stateMutability":"view","type":"function"},{"inputs":[],"name":"refundETH","outputs":[],'
        '"stateMutability":"payable","type":"function"},{"inputs":[{"internalType":"address","name":"from",'
        '"type":"address"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256",'
        '"name":"tokenId","type":"uint256"}],"name":"safeTransferFrom","outputs":[],"stateMutability":"nonpayable",'
        '"type":"function"},{"inputs":[{"internalType":"address","name":"from","type":"address"},'
        '{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"tokenId",'
        '"type":"uint256"},{"internalType":"bytes","name":"_data","type":"bytes"}],"name":"safeTransferFrom",'
        '"outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address",'
        '"name":"token","type":"address"},{"internalType":"uint256","name":"value","type":"uint256"},'
        '{"internalType":"uint256","name":"deadline","type":"uint256"},{"internalType":"uint8","name":"v",'
        '"type":"uint8"},{"internalType":"bytes32","name":"r","type":"bytes32"},{"internalType":"bytes32","name":"s",'
        '"type":"bytes32"}],"name":"selfPermit","outputs":[],"stateMutability":"payable","type":"function"},'
        '{"inputs":[{"internalType":"address","name":"token","type":"address"},{"internalType":"uint256",'
        '"name":"nonce","type":"uint256"},{"internalType":"uint256","name":"expiry","type":"uint256"},'
        '{"internalType":"uint8","name":"v","type":"uint8"},{"internalType":"bytes32","name":"r","type":"bytes32"},'
        '{"internalType":"bytes32","name":"s","type":"bytes32"}],"name":"selfPermitAllowed","outputs":[],'
        '"stateMutability":"payable","type":"function"},{"inputs":[{"internalType":"address","name":"token",'
        '"type":"address"},{"internalType":"uint256","name":"nonce","type":"uint256"},{"internalType":"uint256",'
        '"name":"expiry","type":"uint256"},{"internalType":"uint8","name":"v","type":"uint8"},'
        '{"internalType":"bytes32","name":"r","type":"bytes32"},{"internalType":"bytes32","name":"s",'
        '"type":"bytes32"}],"name":"selfPermitAllowedIfNecessary","outputs":[],"stateMutability":"payable",'
        '"type":"function"},{"inputs":[{"internalType":"address","name":"token","type":"address"},'
        '{"internalType":"uint256","name":"value","type":"uint256"},{"internalType":"uint256","name":"deadline",'
        '"type":"uint256"},{"internalType":"uint8","name":"v","type":"uint8"},{"internalType":"bytes32","name":"r",'
        '"type":"bytes32"},{"internalType":"bytes32","name":"s","type":"bytes32"}],"name":"selfPermitIfNecessary",'
        '"outputs":[],"stateMutability":"payable","type":"function"},{"inputs":[{"internalType":"address",'
        '"name":"operator","type":"address"},{"internalType":"bool","name":"approved","type":"bool"}],'
        '"name":"setApprovalForAll","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{'
        '"internalType":"bytes4","name":"interfaceId","type":"bytes4"}],"name":"supportsInterface","outputs":[{'
        '"internalType":"bool","name":"","type":"bool"}],"stateMutability":"view","type":"function"},{"inputs":[{'
        '"internalType":"address","name":"token","type":"address"},{"internalType":"uint256","name":"amountMinimum",'
        '"type":"uint256"},{"internalType":"address","name":"recipient","type":"address"}],"name":"sweepToken",'
        '"outputs":[],"stateMutability":"payable","type":"function"},{"inputs":[],"name":"symbol","outputs":[{'
        '"internalType":"string","name":"","type":"string"}],"stateMutability":"view","type":"function"},{"inputs":[{'
        '"internalType":"uint256","name":"index","type":"uint256"}],"name":"tokenByIndex","outputs":[{'
        '"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},'
        '{"inputs":[{"internalType":"address","name":"owner","type":"address"},{"internalType":"uint256",'
        '"name":"index","type":"uint256"}],"name":"tokenOfOwnerByIndex","outputs":[{"internalType":"uint256",'
        '"name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{'
        '"internalType":"uint256","name":"tokenId","type":"uint256"}],"name":"tokenURI","outputs":[{'
        '"internalType":"string","name":"","type":"string"}],"stateMutability":"view","type":"function"},{"inputs":['
        '],"name":"totalSupply","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],'
        '"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"from",'
        '"type":"address"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256",'
        '"name":"tokenId","type":"uint256"}],"name":"transferFrom","outputs":[],"stateMutability":"nonpayable",'
        '"type":"function"},{"inputs":[{"internalType":"uint256","name":"amount0Owed","type":"uint256"},'
        '{"internalType":"uint256","name":"amount1Owed","type":"uint256"},{"internalType":"bytes","name":"data",'
        '"type":"bytes"}],"name":"uniswapV3MintCallback","outputs":[],"stateMutability":"nonpayable",'
        '"type":"function"},{"inputs":[{"internalType":"uint256","name":"amountMinimum","type":"uint256"},'
        '{"internalType":"address","name":"recipient","type":"address"}],"name":"unwrapWETH9","outputs":[],'
        '"stateMutability":"payable","type":"function"},{"stateMutability":"payable","type":"receive"}]',
    address='0xC36442b4a4522E871399CD717aBDD847Ab11FE88',
    deployed_block_height=12369651
)


all_contract_configs = [hex_contract_dict, hedron_contract_dict, hex_stake_instance_dict, pulsedogecoin_contract_dict,
                        maximus_contract_dict]
