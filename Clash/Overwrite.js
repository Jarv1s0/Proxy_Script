function main(params) {
//DNS 常量
const defaultDNS = ["223.5.5.5", "119.29.29.29", "1.1.1.1", "8.8.8.8"];
const chinaDNS = ["https://doh.pub/dns-query", "https://dns.alidns.com/dns-query"];
const foreignDNS = ["https://dns.google/dns-query", "https://cloudflare-dns.com/dns-query"];
const dnsConfig = {
  enable: true,
  listen: ":53",
  ipv6: false,
  "prefer-h3": true,
  "use-hosts": true,
  "use-system-hosts": true,
  "respect-rules": true,
  "enhanced-mode": "fake-ip",
  "fake-ip-range": "198.18.0.1/16",
  "fake-ip-filter": [
  "+.lan",
  "+.local",
  "+.stun.*.*",
  "+.stun.*.*.*",
  "+.stun.*.*.*.*",
  "stun.*.*",
  "stun.*.*.*",
  "stun.*.*.*.*",
  "time.windows.com",
  "time.nist.gov",
  "ntp.*.*",
  "ntp.*.*.*",
  "ntp.*.*.*.*",
  "localhost.ptlogin2.qq.com"
],
  "default-nameserver": ["223.5.5.5", "119.29.29.29", "1.1.1.1", "8.8.8.8"],
  "nameserver": [...chinaDNS, ...foreignDNS],
  "proxy-server-nameserver": [...chinaDNS, ...foreignDNS],
  "nameserver-policy": {
    "geosite:private,cn,geolocation-cn": chinaDNS,
    "geosite:google,youtube,telegram,gfw": foreignDNS,
  },
}
//插入DNS配置
params.dns = { ...dnsConfig };
  
//Sniffer 配置
const snifferConfig = {
  enable: true,
  "force-dns-mapping": true,
  "parse-pure-ip": true,
  "override-destination": false,
  sniff: {
    TLS: { ports: [443, 8443] },
    HTTP: { ports: [80, "8080-8880"] },
    QUIC: { ports: [443, 8443] },
  },
  "force-domain": [],
  "skip-domain": ["Mijia Cloud", "+.oray.com"],
};
//插入域名嗅探配置
params.sniffer = { ...snifferConfig };

// 创建代理组函数，支持隐藏
function createProxyGroup(name, type = "url-test", icon, proxies = [], hidden = true) {
  return {
    name,
    type,
    url: "https://cp.cloudflare.com",
    icon,
    interval: 300,
    tolerance: type === "url-test" ? 200 : undefined,
    timeout: type === "url-test" ? 2000 : undefined,
    lazy: true,
    hidden, // 新增 hidden 字段，默认 true
    proxies: proxies.length > 0 ? proxies : ["DIRECT"],
    strategy: type === "load-balance" ? "consistent-hashing" : undefined,
  };
}
//按正则获取代理名
function getProxiesByRegex(params, regex) {
  return params.proxies.filter(e => regex.test(e.name)).map(e => e.name);
}
//地区正则与图标
const regions = [
  { name: "HongKong", regex: /香港|HK|Hong|🇭🇰/, icon: "https://cdn.jsdelivr.net/gh/Koolson/Qure/IconSet/Color/Hong_Kong.png" },
  { name: "TaiWan", regex: /台湾|TW|Taiwan|Wan|🇹🇼/, icon: "https://cdn.jsdelivr.net/gh/Koolson/Qure/IconSet/Color/Taiwan.png" },
  { name: "Singapore", regex: /新加坡|狮城|SG|Singapore|🇸🇬/, icon: "https://cdn.jsdelivr.net/gh/Koolson/Qure/IconSet/Color/Singapore.png" },
  { name: "Japan", regex: /日本|JP|Japan|🇯🇵/, icon: "https://cdn.jsdelivr.net/gh/Koolson/Qure/IconSet/Color/Japan.png" },
  { name: "America", regex: /美国|US|United States|America|🇺🇸/, icon: "https://cdn.jsdelivr.net/gh/Koolson/Qure/IconSet/Color/United_States.png" },
  { name: "Others", regex: /^(?!.*(?:香港|HK|Hong|🇭🇰|台湾|TW|Taiwan|Wan|🇹🇼|新加坡|SG|Singapore|狮城|🇸🇬|日本|JP|Japan|🇯🇵|美国|US|States|America|🇺🇸|自动|故障|流量|官网|套餐|机场|订阅|年|月)).*$/, icon: "https://cdn.jsdelivr.net/gh/Koolson/Qure/IconSet/Color/World_Map.png" },
];

//策略组
  const proxyGroups = regions.map(region =>
    createProxyGroup(region.name, "url-test", region.icon, getProxiesByRegex(params, region.regex))
  );
const predefinedGroups = [
  { name: "Final", type: "select", proxies: ["DIRECT", "Proxy"], icon: "https://cdn.jsdelivr.net/gh/Koolson/Qure/IconSet/Color/Final.png" },   
  { name: "Proxy", type: "select", proxies: ["Fallback", "HongKong", "TaiWan", "Singapore", "Japan", "America", "Others"], icon: "https://cdn.jsdelivr.net/gh/Koolson/Qure/IconSet/Color/Proxy.png" },
  { name: "Fallback", type: "fallback", proxies: ["HongKong", "TaiWan", "Singapore", "Japan", "America", "Others"], url: "https://cp.cloudflare.com", interval: 300, icon: "https://cdn.jsdelivr.net/gh/Koolson/Qure/IconSet/Color/Available.png" }, 
  { name: "AI", type: "select", proxies: ["America", "Japan", "Singapore", "TaiWan", "HongKong", "Others"], icon: "https://cdn.jsdelivr.net/gh/Koolson/Qure/IconSet/Color/ChatGPT.png" },
  { name: "YouTube", type: "select", proxies: ["HongKong", "TaiWan", "Singapore", "Japan", "America", "Others"], icon: "https://cdn.jsdelivr.net/gh/Koolson/Qure/IconSet/Color/YouTube.png" },
  { name: "Telegram", type: "select", proxies: ["HongKong", "TaiWan", "Singapore", "Japan", "America", "Others"], icon: "https://cdn.jsdelivr.net/gh/Koolson/Qure/IconSet/Color/Telegram.png" },
  { name: "Google", type: "select", proxies: ["HongKong", "TaiWan", "Singapore", "Japan", "America", "Others"], icon: "https://cdn.jsdelivr.net/gh/Koolson/Qure/IconSet/Color/Google.png" },
  { name: "Apple", type: "select", proxies: ["HongKong", "TaiWan", "Singapore", "Japan", "DIRECT"], icon: "https://cdn.jsdelivr.net/gh/Koolson/Qure/IconSet/Color/Apple.png" },
  { name: "Games", type: "select", proxies: ["HongKong", "TaiWan", "Singapore", "Japan", "America", "Others"], icon: "https://cdn.jsdelivr.net/gh/Koolson/Qure/IconSet/Color/Game.png" }
  //{ name: "负载均衡", type: "负载均衡", proxies: ["HongKong", "TaiWan", "Singapore", "Japan", "America", "Others"], url: "https://cp.cloudflare.com", interval: 300, strategy: "consistent-hashing", icon: "https://raw.githubusercontent.com/Orz-3/mini/master/Color/Available.png" },
];
  params["proxy-groups"] = [...predefinedGroups, ...proxyGroups]; //插入分组
  // 插入 geox-url 配置
  params["geox-url"] = {
    geoip: "https://fastly.jsdelivr.net/gh/MetaCubeX/meta-rules-dat@release/geoip.dat",
    geosite: "https://fastly.jsdelivr.net/gh/MetaCubeX/meta-rules-dat@release/geosite.dat",
    mmdb: "https://fastly.jsdelivr.net/gh/MetaCubeX/meta-rules-dat@release/country.mmdb",
    asn: "https://fastly.jsdelivr.net/gh/xishang0128/geoip@release/GeoLite2-ASN.mmdb"
  };
  
  // 规则
  const rules = [
    "RULE-SET,AWAvenueAds,REJECT",
    "DOMAIN-SUFFIX, steamserver.net, DIRECT",
    "GEOSITE,private,DIRECT",
    "RULE-SET,Wecaht,DIRECT",
    "GEOSITE,apple,Apple",
    "GEOSITE,apple-cn,DIRECT",
    "GEOSITE,category-ai-!cn,AI",
    "GEOSITE,steam@cn,DIRECT",
    "GEOSITE,category-games@cn,DIRECT",
    "GEOSITE,category-games,Games",
    "GEOSITE,telegram,Telegram",
    "GEOSITE,github,Proxy",
    "GEOSITE,youtube,YouTube",
    "GEOSITE,google,Google",
    "GEOSITE,cn,DIRECT",
    "GEOSITE,geolocation-!cn,Final",
  //GEOIP规则
    "GEOIP,google,Google",
    "GEOIP,telegram,Telegram",
    "GEOIP,twitter,Proxy",
    "GEOIP,cn,DIRECT",
  //绕过局域网地址
    "IP-CIDR,10.0.0.0/8,DIRECT,no-resolve",
    "IP-CIDR,172.16.0.0/12,DIRECT,no-resolve",
    "IP-CIDR,192.168.0.0/16,DIRECT,no-resolve",
    "IP-CIDR,100.64.0.0/10,DIRECT,no-resolve",
    "IP-CIDR,127.0.0.0/8,DIRECT,no-resolve",
    "MATCH,Final"
  ];
  //插入规则
  params["rules"] = rules;

 //远程规则集通用配置
 const ruleAnchor = {
  ip: { type: 'http', interval: 86400, behavior: 'ipcidr', format: 'text' },
  domain: { type: 'http', interval: 86400, behavior: 'domain', format: 'text' },
 };
 //远程规则提供者
 const ruleProviders = {
  AWAvenueAds: { ...ruleAnchor.domain, url: 'https://raw.githubusercontent.com/TG-Twilight/AWAvenue-Ads-Rule/main/Filters/AWAvenue-Ads-Rule-Clash.yaml' },
  Wecaht: {...ruleAnchor.domain, url: 'https://raw.githubusercontent.com/blackmatrix7/ios_rule_script/master/rule/Clash/WeChat/WeChat.yaml'}
 };
 params["rule-providers"] = { ...ruleProviders }; //插入远程规则
  
return params;
}