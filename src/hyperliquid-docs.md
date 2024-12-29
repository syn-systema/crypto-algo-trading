## About Hyperliquid

**What is Hyperliquid?**

Hyperliquid is a high-performance Layer 1 (L1) blockchain designed from the ground up with optimization in mind. Its core vision is to enable a fully on-chain, open financial system. This system would feature user-built applications interacting with performant native components, all while maintaining a high-quality user experience.

**Key Features and Design:**

*   **High Performance L1:** The Hyperliquid L1 is engineered to handle an entire ecosystem of permissionless financial applications. Crucially, every order, cancellation, trade, and liquidation is processed transparently on-chain, achieving block latencies of less than 1 second.
*   **Scalability:** The chain is currently capable of processing 100,000 orders per second, demonstrating its focus on performance and scalability.
*   **Custom Consensus: HyperBFT:** Hyperliquid leverages a custom consensus algorithm known as HyperBFT. This algorithm is heavily inspired by the Hotstuff protocol and its subsequent iterations. Both the algorithm and networking stack are custom-designed and optimized to support the L1's performance demands and architecture.
*   **On-Chain Financial Ecosystem:**  The goal is to have all order processes happening transparently on-chain.
*   **Native Applications:**
    *   **Hyperliquid DEX:** The flagship native application is the Hyperliquid Decentralized Exchange (DEX). It's a fully on-chain order book perpetuals exchange.
    *   **Future Development:**  Future planned development includes a native token standard, functionality for spot trading, and permissionless liquidity options.

In summary, Hyperliquid is focusing on building a high performant, scalable Layer 1 that aims to support an entire financial ecosystem with all processes happening transparently on-chain through a custom built architecture.

## Hyperliquid L1

### L1 Overview

**Introduction**

The Hyperliquid L1 is a custom-built blockchain designed with a high-performance derivatives exchange as its core, flagship component. The decision to focus on a perpetuals order book exchange was driven by the following key considerations:

*   **Real-World Application:** It represents a complex, real-world application that demands more infrastructure performance than existing Layer 1 solutions can typically handle.
*   **High-Value Vertical:**  Perpetuals exchanges are a very valuable vertical within decentralized finance (DeFi), and many user-built applications can benefit from such infrastructure.
*   **Real User Interaction:** It drives and incentivizes real users to interact directly with the underlying L1 infrastructure.
*  **Driving Optimizations:** The continuous demands of the native perp DEX naturally push the L1 to evolve and optimize, leading to fundamental improvements that general-purpose chains may miss.

**Key Design Principles:**

*   **On-Chain State Management:** The L1 state encompasses all margin and matching engine states. Hyperliquid does not rely on off-chain order books.
*   **Full Decentralization:** A core design principle is complete decentralization, which is maintained through a BFT consensus mechanism that ensures a consistent, single order of transactions.
* Note that all order processes happen transparently on-chain

### Latency

*   **HyperBFT Consensus:** The L1 utilizes an optimized consensus algorithm called HyperBFT, which prioritizes minimizing end-to-end latency.
 *   **End-to-End Latency:**  This latency is measured as the time between sending a request and receiving a committed response.
*   **Performance Metrics:**
    *   For orders initiated from a geographically co-located client, the median end-to-end latency is 0.2 seconds.
    *   The 99th percentile end-to-end latency is 0.9 seconds.
*   **Benefits:** This latency performance allows automated trading strategies from other crypto venues to be easily ported to Hyperliquid with minimal modifications. It also provides retail users with instant feedback through the user interface (UI).

### Throughput

*   **Current Capacity:** The Hyperliquid mainnet currently supports approximately 100,000 orders per second.
*   **Current Bottleneck:** The primary bottleneck is currently the execution layer.
*  **Scalability Potential:** The consensus algorithm and networking stack have the potential to scale to millions of orders per second once execution is optimized to keep up.
*   **Future Optimizations:** There are plans to continue optimizing the execution logic as needed to achieve higher throughput.

## Hyperliquid L1

### HyperEVM (Testnet-only)

**Overview**

*   **Integrated EVM:** The Hyperliquid L1 includes a general-purpose Ethereum Virtual Machine (EVM) as part of its blockchain state.
*   **Not a Separate Chain:** Crucially, the HyperEVM is not a separate blockchain. It is secured by the same HyperBFT consensus mechanism that secures the rest of the Hyperliquid L1.
*   **Direct L1 Interaction:** This integration allows the EVM to directly interact with the native components of the L1, such as spot and perpetual order books.

**Key Benefits:**

*   **Asset Fungibility:** ERC20 tokens are fungible with their corresponding native spot assets on Hyperliquid. This offers a seamless transition between the two.
* **Optimized Trading:** Users can trade project tokens with minimal fees and deep liquidity through the native spot order book.
*   **Unified Asset Use:** Users can seamlessly use the same assets on applications built on the EVM after acquiring them through native L1 components.

**Development Status**

*   The HyperEVM and its interactions with the L1 are currently under active development.

**Further Information:**

*   For the latest technical information about the HyperEVM, please refer to the following documentation link: [https://app.gitbook.com/o/9IEyz6nVB2XCF7KcJ16H/s/yUdp569E6w18GdfqlGvJ/~/changes/484/for-developers/evm](https://app.gitbook.com/o/9IEyz6nVB2XCF7KcJ16H/s/yUdp569E6w18GdfqlGvJ/~/changes/484/for-developers/evm)

## Hyperliquid L1

### Bridge

**Security & Operation**

*   **Validator Set Security:** The Hyperliquid bridge is secured by the same set of validators that secure the Hyperliquid L1.
*  **Deposit Process:**
    *   Deposits sent to the bridge are signed by validators on the L1.
    *   The deposit is credited when signatures representing more than 2/3 of the total staking power have been received and verified.
*   **Withdrawal Process:**
    *   Withdrawals initiated from the L1 are immediately placed in escrow on the L1.
    *   Validators sign these withdrawals as separate L1 transactions.
    *   When signatures representing more than 2/3 of the staking power have been collected, an EVM transaction can be sent to the bridge to request the withdrawal.

**Dispute Period:**

*   **Purpose:**  After a withdrawal is requested, there is a dispute period. This period is designed to identify and prevent malicious withdrawals that do not match the L1 records.
*   **Bridge Lock Mechanism:**  During the dispute period the bridge can be locked if a malicious withdrawal is suspected.
*   **Cold Wallet Unlock:** Unlocking the bridge requires cold wallet signatures from a group of validators weighted towards 2/3 of the total stake.

**Finalization & Payout:**

*   **Finalization Transactions:**  After the dispute period has passed, finalization transactions are initiated.
*   **USDC Distribution:** These transactions distribute the USDC to their corresponding destination addresses on the target chain/network.

**Validator Set Management:**

*   **Synchronized Validator Data:** A similar process is used to maintain the set of active validators and their corresponding stake on the bridge contract, ensuring consistency between L1 and Bridge.

**Withdrawal Fee Structure:**

*   **No Arbitrum ETH Requirement:** Users are not required to have Arbitrum ETH for withdrawals.
*   **Fixed USDC Fee:** Users pay a fixed 1 USDC withdrawal fee on the L1. This fee covers the Arbitrum gas costs incurred by the validators when relaying the withdrawal.

**Audits & Code:**

* **Audited by Zellic:** The bridge and its logic in relation to the L1 staking have been audited by Zellic.
*   **Open Source Code:** The full bridge code is available in the Hyperliquid GitHub repository.
*   **Audit Reports:** Audit reports can be found in the "Audits" section.

In summary, the Hyperliquid bridge is designed to facilitate secure and efficient transfer of assets between Hyperliquid L1 and other blockchains with a robust security mechanism based on a 2/3 majority of the L1 validator set. Additionally, it offers user-friendly design such as not requiring users to have a separate chain gas token to perform withdrawal.

## Hyperliquid L1

### API Servers

**Permissionless Design:**

*   **Open Access:** API servers are permissionless, meaning anyone can run one, other than validating nodes which utilize direct RPC connections.
	*   Specifically, any party with a node RPC will be able to access the network and set up their own API server.
*   **Non-Validating Proxies:** API servers act as non-validating proxies to the network, forwarding requests and information.
*   **Load Balancing Flexibility:** The design allows anyone to create customized API server setups with unique load balancing configurations, as needed.

**API Server Functionality:**

*   **Block Update Monitoring:** API servers listen for blockchain updates.
*   **State Maintenance:** They maintain a processed, in-memory representation of the blockchain state specifically for fast handling of user requests.
*   **Request Handling:** On client requests, they forward those requests to the validator nodes and then relay the response back to the client.

**Benefits:**

*   **Familiar API:** The API server's in-memory state representation allows Hyperliquid to offer an API that's similar to those used by automated traders on centralized exchanges.
*   **Scalability and DDoS Protection:** The permissionless model addresses load balancing and DDoS protection challenges, similar to how sentry nodes function in other network designs.

### REST vs. WebSocket

**Data Sources:**

*   **Two Data Sources:** The API provides two primary sources for data: REST and WebSocket.

*   **REST API:**
      *   Orders and cancellations are relayed to the consensus RPC on the network.
      *    The transactions are then gossiped to all the nodes.
      *   The originating request receives a response when the transaction has been included in a block that is committed.

*   **WebSocket API:**
      *   The WebSocket feed is maintained by a replica state that runs parallel to consensus, pushing updates whenever new blocks are created.

**Performance Differences:**

*   **Load Handling:** REST and WebSocket handle load differently due to their architectural make up.
*   **Consensus Processing:** Consensus operations execute as a separate process on each node.
*   **WebSocket Processing:**  The WebSocket process runs within the same process as the state machine updates.
*   **Timestamp Inconsistency:** Due to the architectural difference in how the systems handle load, timestamps from interleaving both data sources are likely not going to be consistent.

In summary, Hyperliquid uses a permissionless API server model to handle load balancing, provide low-latency data to users, and have an existing standardized API.

## Hyperliquid L1

### Clearinghouse

**Perpetuals Clearinghouse**

*   **Core Component:** The perpetuals clearinghouse is the core component of the Hyperliquid L1 exchange state.
*   **Margin State Management:** It's responsible for managing the perpetuals margin state for each address. This includes tracking:
    *   Balances: Available margin held by each address.
    *   Positions: Open perpetual positions held by each address.

*   **Cross Margin:** 
    *   By default, when they are initially deposited to the address, funds are added to the user’s cross-margin balance.
    *   By default, new positions are opened in cross-margin mode.

*  **Isolated Margin:**
    *   Isolated margin is also supported.
    *   This feature allows the user to allocate margin specifically to a position.
    *  With isolated margin, the liquidation risk of such a position is kept separate and not impacted by other positions on the account.

**Spot Clearinghouse**

*   **Spot State Management:** The spot clearinghouse is analogous to the perpetuals clearinghouse, but it manages the spot user state for each address. This includes tracking:
    *   Token Balances: The amount of each token held by the address.
    *   Holds: Any tokens that are on hold for a specific reason.

In summary, the clearinghouses on Hyperliquid L1 are responsible for managing the margin and position of user accounts for both perp and spot trading. The L1 includes both cross and isolated margin features.

## Hyperliquid L1

### Oracle

**Validator Responsibilities:**

*   **Price Publication:** Validators on the Hyperliquid L1 are responsible for publishing spot oracle prices for each perpetual (perp) asset.
*  **Publishing Frequency:** They publish new oracle prices every 3 seconds.

**Uses of Oracle Prices:**

*   **Funding Rates:** Oracle prices are used for computing funding rates for perpetual contracts.
*   **Mark Price Component:** They are incorporated into the mark price, which is a crucial price for:
    *   Margining: Determining the required margin.
    *   Liquidations: Triggering liquidations of under-margined positions.
    *   TP/SL Orders: Executing take-profit (TP) and stop-loss (SL) orders.

**Spot Oracle Price Calculation:**

*   **Weighted Median:** Each validator computes the spot oracle price for each asset as a weighted median.
*   **Data Sources:**  Prices from the following venues are taken into account: Binance, OKX, Bybit, Kraken, Kucoin, Gate IO, MEXC, and the Hyperliquid spot price.
*   **Weights:** Each venue is assigned the following weights when calculating the median 3, 2, 2, 1, 1, 1, 1, 1 respectively, giving more weight to Binance, OKX, Bybit, and lastly hyperliquid's own spot price.
*  **Primary Market Logic** For perps on assets which have a primary spot market on Hyperliquid, external data sources are not incorporated until sufficient liquidity has been established.

**Final Oracle Price:**

*   **Weighted Median of Validators' Prices:** The final oracle price used by the clearinghouse is a weighted median calculated from each validator's submitted oracle prices.
*   **Stake-Weighted:** The validators are weighted by their respective stake in the network.

**In summary**, Each validators is responsible for publishing an oracle price with data from multiple centralized exchanges (and hyperliquid's own spot price when applicable). The total final price is a weighted median from each validator’s submissions with validator stake being the weight.

## Hyperliquid L1

### Order Book

**On-Chain Order Books:**

*   **L1 Native Feature:** The Hyperliquid L1 includes an order book for each asset, which is a core component of the blockchain's state.
*   **Centralized Exchange Model:** The order book functionality is designed to operate similarly to those used by centralized exchanges.

**Order Properties:**

*   **Price Ticks:** Orders are placed at prices that are integer multiples of the tick size of the given trading pair.
*  **Size Lots:** Orders are at sizes that are integer multiples of the lot size of the given trading pair.

**Order Matching:**

*   **Price-Time Priority:** Orders are matched based on price-time priority. This means that orders are matched with the best priced orders first, first to that price as a tiebreaker.

**Clearinghouse Interaction and Margin Checks:**

*   **Clearinghouse Reference:** Operations on the order book directly interact with a reference to the clearinghouse.
*  **Margin Management:** All position and margin checks are managed by the clearinghouse.
*  **Margin Check #1: Order Placement:** Margin checks happen when a new order is placed to see if there is sufficient margin to open a new position or increase an existing one
*  **Margin Check #2: Order Matching:** Margin checks are performed again on the resting side of each order during each match. This ensures that the margin system remains consistent even when market/oracle prices may fluctuate after the resting order was initially placed.

**Key Takeaway:**

The Hyperliquid L1's order book operates with similar logic as traditional Centralized Exchanges. All positions, margin requirements and checks are handled on the clearing house. Margin checks are performed on order placement and each time that a resting order matches with an incoming order.

## Onboarding

### How to Start Trading

**What do I need to trade on Hyperliquid?**

You can trade on Hyperliquid using either:

1.  **A normal DeFi wallet:** (e.g., MetaMask, Rabby, Coinbase Wallet, etc.)
2.  **An email address login.**

**Requirements for DeFi Wallet Users:**

*   **EVM Wallet:** You will need an EVM compatible wallet.
*   **Setting up an EVM Wallet** If you don't have an EVM wallet, you can easily set one up at: [https://metamask.io/](https://metamask.io/).
    *   Download a wallet extension (e.g. Metamask) for your browser and create a new wallet.
    *   **Secure your recovery phrase:**  Your wallet has a secret recovery phrase (seed phrase). Anyone with access to this information can access your funds. Store your seed phrase in a safe physical location.
*   **USDC and ETH on Arbitrum:**
    *   **USDC:** Used as collateral for trading.
    *   **ETH:** Used for gas fees when depositing USDC *only*. Once on L1, trading is gasless.
    *  **Important:** Ensure you are using native Arbitrum USDC. This is not the same as USDC.e.

**Requirements for Email Login Users:**

*   **Email Address:** All you need is an email address.
*   **USDC Native to Arbitrum:** Ensure you have USDC that is native to Arbitrum for deposit when prompted.

### How do I onboard to Hyperliquid?

**Onboarding with Email Login:**

1.  **Click "Connect" Button:** Click the "Connect" button on the Hyperliquid application.
2.  **Enter Email:** Enter your email address.
3.  **Submit and Verify:** Click "Submit." A 6-digit code will be sent to your email. Type that code to log in.
4. Now that you are logged in, a new blockchain address will be created for your email.
5. Send native USDC over the Arbitrum network to the address that is newly created for your email/account. You can do it from a CEX or another wallet.
6.  **Important:** Do not send any asset other than native Arbitrum USDC to this address.

**Onboarding with a DeFi Wallet:**

1.  **Wallet Setup:** Ensure you have an EVM wallet with USDC and ETH on the Arbitrum network.
2.  **Go to Hyperliquid App:**  Navigate to: [https://app.hyperliquid.xyz/trade](https://app.hyperliquid.xyz/trade).
3.  **Switch to Arbitrum Network:** Select the Arbitrum network in your wallet.
4.  **Connect Wallet:** Click "Connect" and choose your wallet type from the popup that appears.
5.  **Confirm Connection:** Approve the connection request in your wallet extension.
6.  **Enable Trading:** Click the "Enable Trading" button.
7.  **Establish L1 Connection:** A modal will appear with two steps. Sign the first transaction in your EVM wallet to confirm a connection with the Hyperliquid L1. This transaction has no gas cost.
8.  **Deposit USDC:** Enter the amount of USDC you want to deposit and click “Deposit”. This transaction will cost ETH on the Arbitrum network. Confirm the transaction.
9.  **Start Trading:** You are now ready to trade on Hyperliquid.

### How do I place a trade on Hyperliquid?

1.  **Token Selection:** Choose a token you want to trade.
2.  **Long or Short:** Decide whether your are going to long or short, depending on whether you predict the price to increase or decrease respectively.
3.  **Position size:** Enter the position size. Remember that position size is calculated by multiplying your leverage by your USDC collateral.
4.  **Place Order:** Tap the "Place Order" button, and tap "Confirm" to confirm the order. Optionally, you can tap "Don't show this again" to prevent having to confirm every trade.

### How do I bridge USDC onto Hyperliquid?

*   **Arbitrum Network:** You first need to get ETH (for gas) and native USDC onto the Arbitrum network.
  *   You can use the official Arbitrum bridge: [https://bridge.arbitrum.io/](https://bridge.arbitrum.io/)
    *   Or the Squid router [https://app.squidrouter.com/](https://app.squidrouter.com/)
  *   Alternatively, you can transfer funds directly to Arbitrum from a centralized exchange if you have access to one.
*   **Important:** Ensure you are bridging *native* USDC to the Arbitrum network (not USDC.e).
*   **Deposit to Hyperliquid:** Once on Arbitrum, you can deposit *native* USDC to the Hyperliquid L1 during the “Enable Trading” process or at any time by clicking the "Deposit" button at the top right of: [https://app.hyperliquid.xyz/trade](https://app.hyperliquid.xyz/trade).

### How do I withdraw USDC from Hyperliquid?

1.  **Navigate to Withdraw:** At: [https://app.hyperliquid.xyz/trade](https://app.hyperliquid.xyz/trade), click the “Withdraw” button in the bottom right corner.
2.  **Enter Amount:** Enter the amount of USDC you want to withdraw.
3.  **Withdraw from L1:** Click the “Withdraw from L1” button.
4.  **Transaction Details:**
    *   The withdrawal transaction itself does not cost gas.
    *   Instead there is a flat $1 USDC withdrawal fee.

## Trading

### Perpetual Assets

**Supported Assets:**

*   **100+ Assets:** Hyperliquid currently supports trading of over 100 perpetual contract assets.
*   **Community-Driven Listings:** New assets are added based on community input and demand.
*   **Future Decentralized Listings:** Hyperliquid plans to implement a decentralized and permissionless process for listing new assets in the future.

**Leverage:**

*   **Variable Leverage:** The maximum leverage available varies by asset.
*   **Leverage Range:** Leverage ranges from 3x to 50x.

**Maintenance Margin:**

*   **Half of Initial Margin:** The maintenance margin is half of the initial margin requirement when using maximum leverage.
*   **Example:** If the maximum leverage for an asset is 20x, the maintenance margin is 2.5% (which is half of 5%, which is 1 / 20).

## Trading

### Contract Specifications

**Perpetual Contracts:**

*   **Derivatives Without Expiration:** Hyperliquid perpetual contracts are derivative products without an expiration date.
*   **Funding Mechanism:** They use funding payments to maintain convergence with the underlying spot price over time. See the section on "Funding" for more information about these payments.

**Margining Style:**

*   **USDC Margined:** Hyperliquid uses USDC as collateral for perpetual contracts.
*   **USDT Denominated Linear Contracts:** The contracts are considered USDT-denominated linear contracts, where the oracle price is denominated in USDT and P&L are calculated in USDT, but collateral is USDC.
*   **No Conversions:**  No explicit conversions are applied between USDC and USDT, making these technically quanto contracts. Profits and losses (P&L) calculated in USDT are paid in USDC.

**USDC-Denominated Oracle Prices**
* When spot asset's primary source of liquidity is USDC denominated, the oracle price is denominated in USDC.
*   Currently, PURR-USD and HYPE-USD are the only native USDC denominated perps as their liquidity is primarily on the Hyperliquid spot.

**Contract Simplicity:**

*   **Simplified Specifications:** Hyperliquid contracts are simpler compared to other platforms, with fewer contract-specific details and no address-specific restrictions.

**Detailed Contract Specifications:**

| Specification         | Details                                                                                          |
| :-------------------- | :----------------------------------------------------------------------------------------------- |
| **Instrument Type**   | Linear perpetual                                                                                 |
| **Contract**          | 1 unit of the underlying spot asset                                                             |
| **Underlying Asset/Ticker** | Hyperliquid oracle index of the underlying spot asset                                             |
| **Initial Margin Fraction** | 1 / (leverage set by user)                                                                     |
| **Maintenance Margin Fraction** | Half of the maximum initial margin fraction (at max leverage for that asset)                                     |
| **Mark Price**        | See the "Mark Price" section for detailed information.                                                |
| **Delivery/Expiration**      | N/A (funding payments occur every hour)                                                                |
| **Position Limit**    | N/A                                                                                            |
| **Account Type**      | Per-wallet cross or isolated margin.                                                              |
|  **Funding Impact Notional** | 20000 USDC for BTC and ETH, 6000 USDC for all other assets
| **Maximum Market Order Value** | $4000000 for max leverage >= 50, $1000000 for max leverage in [20, 50), $500000 for max leverage in [10, 20), otherwise $250000.
| **Maximum Limit Order Value** | 10 * Maximum Market Order Value

## Trading

### Fees

**Fee Structure:**

*   **Volume-Based Fees:** Starting March 11th, trading fees are calculated based on your rolling 14-day trading volume. The first day for which volume counts toward fee tracking was February 26th.
*   **Sub-Accounts:** Sub-account volume contributes to the master account’s volume. All sub-accounts share the same fee tier.
* **Vaults:** Vault volume is tracked and treated separately from the master account, without being combined with the master or sub accounts.
*   **Referral Limitations:** Referral discounts and referral rewards only apply to your first $25 million in trading volume.

**Maker Rebates & Payouts:**

*   **Continuous Rebates:** Maker rebates are paid out continuously on each trade, and get credited directly to the trading wallet
*   **Referral Rewards:** Users can claim referral rewards on the Referrals page of the app.

**Fee Allocation:**

*   **Community-Focused:** All trading fees are directed to the Hyperliquid community, specifically to HLP (Hyperliquid Points) and the assistance fund.
*   **Assistance Fund:** This fund operates as part of the core L1 execution.
    *   The assistance fund is held on the 0xfefefefefefefefefefefefefefefefefefefefe address.
    *   The assistance fund uses the system address and requires validator quorum to use in special situations. The majority of its balance is held in HYPE.

**Historical Fee Structure:**

*   **Zero-Fee Period:** For the first three months of the mainnet closed alpha, there were no gas or trading fees.
*   **Initial Fees:** In June 2023, a flat fee of 2.5 bps (0.025%) for takers and a rebate of 0.2 bps (0.002%) for makers was introduced.
*   **Referral Rewards:** During the period when fee were flat, Referrers received 10% of their referees’ taker fees.

## Trading

### Builder Codes

**Note on "Builder" Terminology:**
*In this context, "builder" refers to DeFi builders who develop applications on the Hyperliquid L1, and NOT block builders within consensus.*

**Functionality:**

*   **Fee Sharing:** Builder codes allow builders (application developers) to receive a portion of the trading fees for fills they generate on behalf of users.
*   **Per-Order Flexibility:** Builder codes can be set on a per-order basis, offering maximal flexibility.
*   **User Approval:** Before using a builder code, users must explicitly approve a maximum fee for each builder.
*   **Revocable Permissions:** Users can revoke builder permissions at any time.
*   **On-Chain Processing:** Builder codes are processed entirely on-chain as part of the L1's fee logic.

**Implementation:**

1.  **User Approval (ApproveBuilderFee Action):**
    *   Users must approve a maximum fee for a builder by sending an `ApproveBuilderFee` action.
    *   This action must be signed by the user's main wallet (not an agent or API wallet).
2.  **Builder Requirements:**
    * Builders are required to hold at least 100 USDC in perp account value to participate in the builder program.
3.  **Builder Fee Application:**
    *   Builder codes only apply to fees collected in USDC.  They do not apply to the buying side of spot trades.
    *   Builder fees cannot exceed 0.1% on perpetuals and 1% on spot trades.
4.  **Order Action Parameters:**
    *   Future order actions sent on a user's behalf can include an optional builder parameter: `{"b": address, "f": number}`
        *   `b`: The address of the builder.
        *  `f`: The builder fee to charge, given in tenths of basis points. (e.g. 10 means 1 basis point).
5.  **Fee Claiming:**
    *   Builders can claim their earned fees through the standard referral reward claim process.

**Example Code:**

*   Refer to the Python SDK for code examples: [https://github.com/hyperliquid-dex/hyperliquid-python-sdk/blob/master/examples/basic_builder_fee.py](https://github.com/hyperliquid-dex/hyperliquid-python-sdk/blob/master/examples/basic_builder_fee.py)

**API for Builders:**

*   **Querying Approved Maximum Fee:** Use the `info` request `{"type": "maxBuilderFee", "user": "0x...", "builder": "0x..."}` to query the maximum approved builder fee for a specific user and builder.
*   **Total Builder Fees:** The total collected fees for a builder can be found as part of the referral state by an `info` request with `{"type": "referral", "user": "0x..."}`
*   **Trade Data:** Trade data associated with builder codes are uploaded weekly in compressed LZ4 format to: `https://stats-data.hyperliquid.xyz/Mainnet/builder_fills/{builder_address}/{YYYYMMDD}.csv.lz4`
    *   Example: `https://stats-data.hyperliquid.xyz/Mainnet/builder_fills/0x123.../20241031.csv.lz4`
    *   Builder information is accessible in the Mainet folder only.

**In summary**, Builder codes allow those that build on Hyperliquid to get referral fees for orders that they bring to the L1. This process is transparent and permissionless.

## Trading

### Order Types

**Basic Order Types:**

*   **Market Order:**
    *   Executes immediately at the current market price.
*   **Limit Order:**
    *   Executes at the selected limit price or a better price.
*   **Stop Market Order:**
    *   A market order that is activated when the price reaches a selected stop price.
    *   Often used to limit losses or lock in profits.
*   **Stop Limit Order:**
    *   A limit order that is activated when the price reaches a specified stop price.
*   **Scale Order:**
    *   Places multiple limit orders within a defined price range.
*   **TWAP (Time-Weighted Average Price) Order:**
    *   Divides a large order into smaller suborders.
    *   Executes these suborders at 30-second intervals.
    *   Has a maximum slippage of 3% per suborder.

**TWAP Order Details**
   * **Execution Target:** TWAP orders aim to match a target execution rate based on elapsed time compared to the total time.
    *   **Suborders:** Sends a suborder every 30 seconds.
    *   **Max Slippage:** Suborders are constrained to a maximum slippage of 3%.
    *   **Catch-Up Logic:** If suborders don't fully fill, the TWAP attempts to catch up in later suborders with a size of at most 3 times the normal suborder size.
    *   **Potential for Partial Fill:** If many suborders did not fill, TWAP may not fully achieve the total target size by the end.
     *   **Post-Only Period Inactivity:** TWAP suborders will not fill during the "post-only" period of any network upgrades.

**Order Options:**

*   **Reduce Only:**
    *   An order that is restricted from opening new positions on the opposite side.
    *   Primarily used to reduce a current position.
*   **Good Til Cancel (GTC):**
    *   An order that remains active (resting on the order book) until it is either filled or manually canceled.
*   **Post Only (ALO - Add Limit Order):**
    *   An order that is added to the order book but will never execute immediately as a taker.
    *   Only executed as a maker/resting order.
*  **Immediate Or Cancel (IOC):**
    * An order that is fully filled at any price or cancelled immediately.
*   **Take Profit (TP):**
    *   An order that is activated when a predetermined take-profit price is reached.
    *   TP is executed as a market order.
*   **Stop Loss (SL):**
    *   An order that is activated when a predetermined stop-loss price is reached.
    *   SL is executed as a market order.

**TP/SL Order Functionality**

*   **Purpose:** TP/SL orders are commonly used to help traders set profit targets and minimize potential losses.
*   **Market Order Type** By default, TP/SL orders are automatically market orders.
*   **Limit Price & Partial Size:** User can set a limit price and configure an amount of their position for TP/SL orders.

## Trading

### Take Profit and Stop Loss Orders (TP/SL)

**Functionality:**

*   **Position Closure:** TP/SL orders are designed to automatically close a position when a specified profit (TP) or loss (SL) level is reached.
*   **Mark Price Trigger:** The mark price is used to determine when a TP/SL order should be triggered.

**TP/SL Order Interaction on the Chart**

*   **Drag and Drop:** TP/SL orders can be interactively adjusted by dragging them on the TradingView chart. There is often a slight delay in between the user drag and the new order being placed.
*  **Immediate Execution Prevention:** Dragging a TP/SL order in a way that causes an immediate execution will result in an error that prevents the trade from being placed. This error is intended to prevent user mistakes.
* **Manual Closure Option:** If immediate execution is desired, an order can be closed manually from the position table or via the order form.

**Limit vs. Market TP/SL Orders:**

*   **Choice of Order Type:** Users can choose between market or limit orders for their TP/SL.
*   **Market TP/SL Slippage Tolerance:** TP/SL market orders have a slippage tolerance of 10%.
*  **Limit Price Control:**  By setting a limit price on a TP/SL order, you can control order slippage. The more aggressive the limit price is, the more likely it is to completely fill, at the cost of a greater potential slippage.
* **Example Scenario:** A stop loss (SL) order to close a long position with a trigger price of $10 and a limit price of $10 will hit the book when the mark price drops below $10. If the price drops from $11 to $9 instantaneously, the stop loss order would likely rest on the orderbook at $10 instead of immediately filling. However, giving the order a limit price of $8 rather than $10 means that the order is more likely to fill for a price point somewhere between $8 and $9.

**TP/SL Associated with a Position:**

*   **Default Size:** TP/SL orders created from the position form will have a size set to the current position size by default.
*  **Position Size Handling:** TP/SL orders set to the default size attempt to close the entire position upon triggering.
* **Fixed-Sized Option:** Specifying a specific size on a TP/SL order makes it a fixed size that will not resize with changes to the position after it has been placed.
*   **Beginner-Friendly:** These TP/SL orders are straightforward to place and cancel.

**TP/SL Associated with a Parent Order (OCO - One Cancels Other):**

*   **Fixed Size to Parent:**  TP/SL orders created from the order form have a fixed size equal to the parent order they are tied to.
*   **Immediate Placement:** If the parent order is completely filled, the linked TP and/or SL orders are placed immediately, this is the same behavior as a position tied TP/SL order.
*   **Untriggered State:** If the parent order is not fully filled, the TP/SL orders remain in an untriggered state until the parent order has been fully filled or cancelled due to insufficient margin. In this state, the TP/SL orders have not been submitted and are not visible on the charts.
     * The TP/SL order will not get placed and will cancel if the parent is manually cancelled.
*  **Cancellation Logic:**
    *  If a user manually cancels a partially filled parent order, any associated child TP/SL orders are also canceled. To have a TP/SL on the partially filled portion, they have to be re-created as a position TP/SL linked to the new position.
* **Exceptions to Cancellation Logic:** TP/SL will be placed if and only if a parent order is fully filled or when a partially filled order is canceled due to insufficient margin. In the case of the latter, the fixed size will match the size the parent order attempted to placed.

**In conclusion:**

*   TP/SL orders provide automated trade closure at specified profit/loss levels.
* Both market and limit versions of TP/SL are available.
* TP/SL can be created independent from a position, or tied to a specific order.
* TP/SL orders have unique behaviors depending on whether it is linked to a position, or tied to an order as an OCO order.

## Trading

### Margining

**Overview**
* Margin calculations are based on common formulas already utilized by major centralized derivatives exchanges.

**Margin Modes**

*   **Cross Margin**
    *   Default mode.
    *   Maximizes capital efficiency by allowing all cross margin positions to share collateral.
*   **Isolated Margin**
    *   Limits the collateral to the specific asset.
    *   Liquidations in isolated margin do not affect other isolated or cross-margin positions.
    *   Liquidations in cross margin do not impact isolated positions.

**Initial Margin and Leverage**

*   **Leverage Setting:** Users can set leverage at any integer between 1 and the maximum allowed leverage for a given asset.
*   **Max Leverage:**  Maximum leverage is determined by each individual asset.
*   **Initial Margin Calculation:** `position_size * mark_price / leverage`
*   **Cross Margin:** Initial margin cannot be withdrawn when a cross margin position is open.
*   **Isolated Margin:** Allows for adding and removing margin while a position is already open.
*   **Unrealized PnL**
    *   **Cross Margin:**  Unrealized PnL automatically becomes available as an initial margin for new positions.
    *   **Isolated Margin:** Unrealized PnL is added as additional margin for active positions.
*   **Increasing Leverage:** You can increase the leverage on an existing position without closing it
*   **Leverage Checks:** Checks for the user-selected leverage only occur when a position is opened.
*   **User Responsibility:** Users are responsible for monitoring their leverage to avoid liquidation.
*   **Actions for Negative PnL:** Users can close a position, add margin (if isolated), or deposit USDC (if cross) to manage positions with negative unrealized PnL.

**Maintenance Margin and Liquidations**

*   **Cross Position Liquidation:** Liquidations occur when the cross position's account value (including unrealized PnL) falls below the maintenance margin multiplied by the total open notional position.
*   **Isolated Position Liquidation:** Isolated positions are liquidated using the same maintenance margin logic, only considering the isolated position's margin and notional value.
*   **Maintenance Margin:** Set to half of the initial margin required at max leverage.

## Trading

### Liquidations

**Overview**

- **Liquidation Event:** Triggered when a trader’s positions shift adversely, causing account equity to dip below the maintenance margin. 
- **Maintenance Margin:** It's set at half of the initial margin required at maximum leverage, ranging from 1% for 50x leverage assets to 16.7% for 3x leverage assets, based on the asset type.

**Liquidation Process**

1. **Initial Market Order Attempt:**
   - A market order is issued to close the full size of the position. 
   - The order may result in partial or full closure.
   - Remaining collateral stays with the trader if maintenance margin requirements are met by the position's partial/full closure.
   
2. **Backstop Liquidation:**
   - If account equity falls below 2/3 of the maintenance margin and liquidation through the market order hasn't succeeded, a backstop liquidation through the liquidator vault occurs.
   - **Cross Position:** All cross positions and margin are transferred to the liquidator.
   - **Isolated Position:** Only the isolated position and margin are transferred, leaving cross margin positions unchanged.
   - **Maintenance Margin:** It isn’t returned to the user during a backstop liquidation, as the liquidator vault needs it as a buffer for average profitability.

3. **Proactive Measures:**
   - To avoid losing maintenance margin, traders can place stop-loss orders or exit positions before reaching the liquidation mark price.

**Liquidation Mechanics**

- **Mark Price Utilization:** Liquidations use a mark price combining CEX prices with Hyperliquid's book state, making them more robust than single price sources.
- **Volatility Consideration:** During high volatility, mark price can significantly diverge from the book price. The exact formula is recommended for precise monitoring.

**Liquidator Vault**

- **Democratized Process:** The liquidator vault democratizes backstop liquidations as part of HLP's strategy.
- **Profit Allocation:** On Hyperliquid, liquidation profits benefit the community via HLP, whereas, on other venues, they often benefit the exchange operators or privileged market makers.

**Computing Liquidation Price**

- **Estimate Display:** An estimated liquidation price is shown when entering a trade, which might be inaccurate due to liquidity changes.
- **Post-Entry Liquidation Price:** Displayed after opening a position but may deviate due to funding payments or unrealized PnL alterations in other cross margin positions.
- **Leverage Dependence:** 
  - Cross positions: Actual liquidation price unaffected by leverage, using more collateral if leverage is lower.
  - Isolated positions: Dependent on leverage, as isolated margin allocation is based on the initial margin.

**Liquidation Price Formula:**
liq_price = price - side * margin_available / position_size / (1 - l * side)


- Where:
  - `l` = `1 / MAINTENANCE_LEVERAGE`
  - `side` = `1` for long, `-1` for short
  - `margin_available (cross)` = `account_value - maintenance_margin_required`
  - `margin_available (isolated)` = `isolated_margin - maintenance_margin_required`

## Trading

### Entry Price and PNL

On the Hyperliquid DEX, entry price, unrealized PNL, and closed PNL are primarily front-end components for user convenience. Core accounting is based on margin and trades.

#### Perpetual Contracts (Perps)

- **Opening Trades:** 
  - **Definition:** Considered opening when the absolute position value increases (longing while already long or shorting while already short).
  - **Entry Price Update:** Updated to a weighted average between the current entry price and trade price based on trade size.
  
- **Closing Trades:**
  - **Entry Price:** Remains unchanged.
  
- **Unrealized PNL Calculation:**
  - Formula: `unrealized_pnl = side * (mark_price - entry_price) * position_size`
  - Where `side = 1` for long positions and `side = -1` for short positions.

- **Closed PNL Calculation:**
  - Formula for closing trade: `fee + side * (mark_price - entry_price) * position_size`
  - For opening trades, only the fee is considered.

#### Spot Trades

- **Similarities to Perps:** 
  - Use the same PNL formulas with adaptations for spot trade logic.
  
- **Trade Classification:**
  - **Opening:** Buys are considered opening.
  - **Closing:** Sells are considered closing.
  
- **Transfer Treatments:** 
  - Treated as buys or sells at mark price.
  
- **Genesis Distributions:**
  - Entry price set at a market cap of 10,000 USDC.
  - Avoids undefined return on equity by not setting a 0 entry price since they are not bought.

- **Pre-existing Spot Balances:**
  - Assigned an entry price from the first trade or send post-feature enablement, around July 3, 08:00 UTC. 

## Trading

### Funding

**Overview**

- **Purpose of Funding Rates:** Used to keep the perpetual contract's price aligned with the underlying asset's spot price via periodic peer-to-peer payments between the long and short positions.
- **Interest Rate Component:** Predetermined at 0.01% every 8 hours, equating to 0.00125% every hour or 11.6% annual percentage rate (APR) paid to shorts, reflecting USD borrowing costs versus spot crypto.
- **Premium Component:** Based on the price difference between the perpetual contract and the underlying spot oracle price.
  - Positive premium: Long pays short.
  - Negative premium: Short pays long.
- **Funding Rate Frequency:** Calculated and applied every hour. 

**Technical Details**

- **Consistency with Centralized Exchanges (CEXs):** Funding computation is modeled closely after CEX methodologies.
- **8-Hour Funding Rate Usage:** While the overall rate is based on an 8-hour computation, it's applied every hour at one-eighth of this rate.
- **Formula:** 
Funding Rate (F) = Average Premium Index (P) + clamp (interest rate - Premium Index (P), -0.0005, 0.0005)

- **Premium Sampling:** Conducted every 5 seconds and averaged over the hour.
- **Oracle Prices:** Weighted median of CEX spot prices, with weights based on CEX liquidity.
- `premium = impact_price / oracle_price - 1`
- `impact_price` includes adjustments for `impact_bid_px` and `impact_ask_px`. 
- Refer to contract specifications for detailed impacts and notional values.

- **Funding Cap:** 4% per hour, less aggressive compared to CEXs. 
- **Payment Calculation:**
funding_payment = position_size * oracle_price * funding_rate

- Uses the spot oracle price instead of the mark price to convert position size to notional value.

**Numerical Example**

- **Interest Rate:** Fixed at 0.01%.
- **Example Scenario:** 
- Perpetual contract premium exists with an impact bid price of $10,100 and a spot price of $10,000.
- Calculated premium index as $100 or 1% in this context.
- You hold a long position of 10 contracts (each representing 1 BTC).
- **Premium Calculation:**
Premium = (Impact bid price - Spot Price) / Spot Price
= ($10,100 - $10,000) / $10,000
= 0.01 or 1%

- **Interest Rate Clamping:**
Clamped Difference = min(max(Interest Rate - Premium Rate, -0.05%), 0.05%)
= min(max(0.01% - 1%, -0.05%), 0.05%)
= -0.05%

- **Funding Rate Calculation:**
Funding Rate = Premium Rate + Clamped Difference
= 1% + (-0.05%)
= 0.95%

## Trading

### Auto Deleveraging

**Overview**

- **Purpose:** Auto-deleveraging is used as a last resort mechanism to prevent liquidations that could result in a significant platform drawdown, thereby strictly ensuring platform solvency.
- **Trigger:** Activated when a user's account value or isolated position value turns negative. 
- **Action:** 
  - Positions of traders on the opposite side of the underwater position are closed at the previous oracle price. 
  - This closure is based on ranking by unrealized PNL and leverage used.
- **Solvency Assurance:** Ensures that the platform remains free of bad debt through this mechanism, maintaining overall financial stability.

**Key Points**

- **User Protection:** A core invariant of the system is that users without open positions will not be affected by losses socialized across the platform.
- **Final Safeguard:** Functions as the platform’s ultimate safeguard to uphold solvency and financial responsibility.

## Trading

### Robust Price Indices

**Overview**

Hyperliquid utilizes robust pricing mechanisms that incorporate order book and external data, helping to mitigate the risk of market manipulation.

**Price Types and Their Usage**

1. **Oracle Price:**
   - **Purpose:** Used for computing funding rates.
   - **Characteristics:** 
     - A weighted median of CEX prices, independent of Hyperliquid's market data.
     - Updated by validators approximately every three seconds.

2. **Mark Price:**
   - **Purpose:** Offers an unbiased and robust estimate of the fair perpetual contract price.
   - **Usage:** Essential for margining, liquidations, triggering TP/SL (Take Profit/Stop Loss), and computing unrealized PNL.
   - **Update Frequency:** Updated whenever validators publish new oracle prices, roughly every three seconds.
   - **Calculation:**
     - Comprises the median of the following:
       - Oracle price plus a 150-second exponential moving average (EMA) of the difference between Hyperliquid's mid-price and the oracle price.
       - Median of best bid, best ask, and last trade on Hyperliquid.
       - Median of Binance, OKX, and Bybit perpetual mid-prices.
     - If exactly two out of the three components exist, the 30-second EMA of the median of best bid, best ask, and last trade on Hyperliquid is also included.

**EMA Update Formula**

The EMA is updated using the following formula whenever there's a new data sample after a duration `t` since the last update:
ema = numerator / denominator

numerator -> numerator * exp(-t / 2.5 minutes) + sample * t

denominator -> denominator * exp(-t / 2.5 minutes) + t


This EMA formula helps in smoothing the price inputs, providing a stable and continuous estimate of pricing trends in the market.

## Trading

### Self-Trade Prevention

**Overview**

- **Mechanism:** In the event of trades between the same address, the resting order is canceled instead of executing a fill.
- **Fee Impact:** No fees are deducted for self-trades.
- **Visibility:** These cancellations do not appear in the trade feed.

**Comparison with CEXs**

- **"Expire Maker" Behavior:** On centralized exchanges (CEXs), this self-trade prevention is often referred to as "expire maker." 
- **Market Making Advantage:** This behavior is advantageous for market making algorithms, allowing the aggressing order to continue filling against liquidity up to the limit price without the interference of self-trades.

## Trading

### Portfolio Graphs

**Overview**

- The portfolio page provides visual representations of account value and P&L over various time frames: 24 hours, 7 days, and 30 days.

**Account Value:**

- **Components:**
  - Includes unrealized PNL from both cross and isolated margin positions.
  - Includes vault balances and other account-held assets.

**Profit and Loss (PnL):**

- **Calculation:** 
  - Defined as `account_value + net_deposits`
  - Formula: `account value + deposits - withdrawals`

**Graph Details:**

- **Sampling:** 
  - Graphs are based on samples collected during deposits, withdrawals, and every 15 minutes.
- **Precision Note:**
  - Due to their sampled nature, the graphs are not recommended for precise accounting.
  - Interpolations between samples may not accurately represent changes in unrealized PNL between consecutive samples.

  ## Trading

### Index Perpetual Contracts

**Overview**

Index perpetual contracts operate similarly to regular perpetual contracts but use a formula-based index rather than tracking a spot asset price. Validators periodically publish the index value to the Hyperliquid L1, where the median of these values is used to compute funding rates instead of a spot oracle.

#### NFTI-USD

- **Description:** An index of select blue-chip NFT collections.
- **Included Collections:** 
  - Bored Ape Yacht Club (BAYC)
  - Mutant Ape Yacht Club (MAYC)
  - Azuki
  - DeGods
  - Pudgy Penguins
  - Milady Maker
- **Index Calculation:**
  - Calculated as a 3-minute EMA of the aggregate floor price.
  - Aggregate Floor Price Formula: 
    ```
    [(BAYC floor price / 10) + (MAYC floor price) + (Azuki floor price) + (DeGods floor price) + (Pudgy Penguins floor price) + (Milady Maker floor price)] / 10000
    ```
  - Floor prices aggregated from OpenSea and Blur, and converted to USDT using the ETH-USDT spot oracle price.
- **Exclusions:** CryptoPunks are excluded due to their status preceding the NFT standard and listing absence on these marketplaces.

#### FRIEND-USD

- **Notability:** First index perpetual contract listed on Hyperliquid.
- **Evolving Criteria:** Initially based on top 20 friendtech index, rebalanced biweekly.
- **Current Tracking (Starting October 4):** Average one-share buy price of the middle 8 subjects among the following 20 accounts:
  - 0xCaptainLevi, Dingalingts, 0xRacerAlt, HsakaTrades, HerroCrypto, HanweChang, Christianeth, 0xLawliette, CL207, Cryptoyieldinfo, CapitalGrug, iloveponzi, cobie, sayinshallah, pokeepandaa, pranksy, VentureCoinist, 0xBreadguy, saliencexbt, blknoiz06.
- **Historical Adjustments:** 
  - September 13 - October 4: Tracked a different set of accounts using median pricing scaled for index continuity.
  - August 23 - September 13: Used an alternate list with scaling adjustments for continuous index transition.
- **Conversion:** Friendtech key prices converted to USDT using ETH/USDT median prices from robust CEXs.

**Additional Information**

- **Index Contract**: View on [BaseScan](https://basescan.org/address/0xcf205808ed36593aa40a44f10c7f7c2f67d4a4d4).

## Trading

### Uniswap Perpetuals

**Overview**

Some perpetual contracts on Hyperliquid derive their underlying spot asset prices from Uniswap V2 or V3 AMM prices. These contracts are designed to be isolated-only, meaning:

- **Margin Characteristics:**
  - **Isolated-Only:** Cross margin is prohibited, and users cannot manually remove margin from an open position.
  - **Margin Adjustment:** To adjust margin, positions must be partially or fully closed, thereby returning the corresponding amount of isolated margin.

**Uniswap Pool Contract Addresses**

- **RLB:** [0x510100d5143e011db24e2aa38abe85d73d5b2177](https://etherscan.io/address/0x510100d5143e011db24e2aa38abe85d73d5b2177)
- **OX:** [0x49727bbe3ba46aeb1058749ed2741a42fd1ccda8](https://etherscan.io/address/0x49727bbe3ba46aeb1058749ed2741a42fd1ccda8)
- **UNIBOT:** [0x8DbEE21E8586eE356130074aaa789C33159921Ca](https://etherscan.io/address/0x8DbEE21E8586eE356130074aaa789C33159921Ca)
- **HPOS:** [0x2cC846fFf0b08FB3bFfaD71f53a60B4b6E6d6482](https://etherscan.io/address/0x2cC846fFf0b08FB3bFfaD71f53a60B4b6E6d6482)
- **SHIA:** [0x81a460ea6fd96a73d5672f1f4aa684697d4b44cc](https://etherscan.io/address/0x81a460ea6fd96a73d5672f1f4aa684697d4b44cc)
- **BANANA:** [0x43DE4318b6EB91a7cF37975dBB574396A7b5B5c6](https://etherscan.io/address/0x43DE4318b6EB91a7cF37975dBB574396A7b5B5c6)

## Trading

### Hyperps

**High-Level Summary**

- **Definition:** Hyperps are a type of perpetual contract available exclusively on Hyperliquid. Unlike standard perpetual contracts, they do not rely on an underlying spot or index oracle price. Instead, the funding rate is based on a moving average Hyperp mark price, enhancing price stability and reducing manipulation potential typically observed in pre-launch futures.
- **Underlying Asset/Index:** There is no need for a constant underlying asset or index throughout a Hyperp's lifetime, but the asset or index must eventually exist for settlement or conversion.
- **Funding Rates:** Crucial in Hyperp trading, especially with strong price momentum. High momentum in one direction incentivizes taking positions in the opposite direction over the next 8 hours.

**Conversion to Vanilla Perps**

- **Trigger for Conversion:** A Hyperp converts to a regular perpetual (e.g., ABC-USD) shortly after the underlying asset (e.g., ABC=ZRO, TIA, PYTH, JUP, W, STRK) is listed for spot trading on platforms like Binance, OKX, or Bybit.

**Open Interest Caps**

- **Initial Cap:** A cap of $1,000,000 open interest was set for Hyperps in assets such as ZRO, TIA, PYTH, JUP, W, and STRK at launch. This cap may be adjusted as market conditions mature.

**Mechanism Details**

- **Operation:** Hyperps function similarly to standard perpetuals, albeit with a distinct pricing mechanism.
- **Oracle Price Calculation:**
  - Replaces external spot/index price with an 8-hour exponentially weighted moving average of minutely mark prices from the previous day.
  - **Formula:** 
    ```
    oracle_price(t) = min[sum_{i=0}^1439 [(t - i minutes < t_list ? initial_mark_price : mark_price(t - i minutes)) * exp(-i/480)] * (1 - exp(-1/480)) / (1 - exp(-3)), initial_mark_price * 4]
    ```
    - `a ? b : c` evaluates to `b` if `a` is true, otherwise `c`.
    - Samples taken one block after each unix minute; timestamps align with nearest exact minute multiples.
    - For fewer than 480 samples, initial mark price provides padding.
- **Safeguards:**
  - Oracle price is bound to 4 times the one-month average mark price to prevent manipulation.

- **Funding Rate Calculation:**
  - Uses 5% of the normal clamped interest rate and premium formula.
  - See [Funding Documentation](#) for detailed calculations.

## Vaults

**Overview**

On Hyperliquid, vaults are advanced and versatile components integrated into the Hyperliquid L1. They leverage the same sophisticated features as the DEX, from managing liquidations of overleveraged accounts to facilitating high-throughput market-making strategies, eliminating the need for simple token rebalancing deposits.

**Key Features**

- **Open Participation:** 
  - Anyone, including DAOs, protocols, institutions, and individuals, can deposit into vaults to share in the profits.
  
- **Profit Sharing:**
  - Vault owners are entitled to 10% of the total profits. 
  - Exception: Protocol vaults are exempt from fees and profit sharing.

- **Management Options:**
  - Can be operated by individual traders or automated by a market maker.
  
- **Risk Consideration:**
  - Each strategy carries inherent risks.
  - Users should evaluate the risk and historical performance of a vault before deciding to deposit.

## Historical Data

Hyperliquid provides historical data in a compressed format, available via S3 storage. This data includes L2 book snapshots and asset context metadata, but does not extend to trades or spot market data. Users interested in additional historical datasets are encouraged to utilize the API for data recording.

### Data Compression and Storage

- **Compression Format:** LZ4
- **Storage Location:** S3 bucket `hyperliquid-archive`
- **Update Frequency:** Approximately once a month

### Data Types and Availability

#### Market Data

- **File Path Format:** 
s3://hyperliquid-archive/market_data/[date]/[hour]/[datatype]/[coin].lz4

- **Example Usage:**
- **Commands:**
  ```bash
  aws s3 cp s3://hyperliquid-archive/market_data/20230916/9/l2Book/SOL.lz4 /tmp/SOL.lz4 --no-sign-request
  unlz4 --rm /tmp/SOL.lz4
  head /tmp/SOL
  ```
- **Requirements:**
  - AWS CLI: [Installation Guide](https://docs.aws.amazon.com/cli/latest/userguide/getting-started-install.html)
  - LZ4: [Installation and Usage](https://github.com/lz4/lz4)

#### Asset Metadata Snapshots

- **File Path Format:**
s3://hyperliquid-archive/asset_ctxs/[date].csv.lz4


**Note:** Historical data sets related to trades or spot markets are not available directly via S3.

## Hyperliquid Python SDK Integration Guide

### Setup and Installation

The Hyperliquid Python SDK has been installed in your environment. You can import it in your Python files using:

```python
from hyperliquid.info import Info
from hyperliquid.exchange import Exchange
from hyperliquid.utils import constants
```

### Key Components

1. **Info Class**: Used for fetching market data and account information
   - Get market states
   - Query positions
   - View order book data

2. **Exchange Class**: Used for executing trades and managing orders
   - Place orders
   - Cancel orders
   - Modify positions

3. **Constants**: Contains important constants like API endpoints

### Example Usage

```python
from hyperliquid.info import Info
from hyperliquid.exchange import Exchange
from eth_account import Account

# Initialize connection
account = Account.from_key(private_key)
info = Info()
exchange = Exchange(account)

# Get market data
market_info = info.meta()

# Place an order
order_params = {
    "coin": "WIF",
    "is_buy": True,
    "sz": 0.01,
    "limit_px": 1000.0,
    "reduce_only": False
}
response = exchange.order(order_params)
```

### Current Integration

The SDK is currently integrated into your project in:
- `src/risk_management/risk_mgmt_hl.py` - Risk management bot
- `src/bots/hyperliquid-bot-1.py` - Trading bot

Both bots use the SDK to interact with Hyperliquid's API for trading and market data.

### Testing

For testing your bots:

1. Start with small position sizes (0.01 contracts)
2. Use conservative risk parameters
3. Monitor positions closely
4. Test one bot at a time:
   - First test the trading bot (`hyperliquid-bot-1.py`)
   - Then add risk management (`risk_mgmt_hl.py`)

### Important Notes

- Always use your private key securely (store in environment variables)
- Test with small positions first
- Monitor your positions when running bots
- Keep track of all open orders and positions