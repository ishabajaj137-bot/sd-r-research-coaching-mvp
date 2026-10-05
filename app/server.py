from http.server import ThreadingHTTPServer,SimpleHTTPRequestHandler
from urllib.parse import urlparse,parse_qs
from pathlib import Path
import json,os
ROOT=Path(__file__).resolve().parent
class H(SimpleHTTPRequestHandler):
 def __init__(self,*a,**k): super().__init__(*a,directory=str(ROOT),**k)
 def out(self,d,s=200):
  b=json.dumps(d).encode();self.send_response(s);self.send_header("Content-Type","application/json");self.send_header("Content-Length",str(len(b)));self.end_headers();self.wfile.write(b)
 def do_GET(self):
  if self.path.startswith("/api/research"):
   c=parse_qs(urlparse(self.path).query).get("company",[""])[0].strip()
   return self.out(research(c) if c else {"error":"Company required"},200 if c else 400)
  return super().do_GET()
 def do_POST(self):
  if self.path!="/api/analyze": return self.send_error(404)
  try:
   n=int(self.headers.get("Content-Length","0"));p=json.loads(self.rfile.read(n) or "{}");return self.out(analyze(p))
  except Exception as e:return self.out({"error":str(e)},400)
def research(c):
 s={"industry":"B2B SaaS","founded":"2014","global_hq":"Singapore","india_presence":"Bengaluru, Hyderabad","employees":"~2,500","status":"Private","description":"Enterprise workflow software","signals":[{"date":"Sep 2026","type":"Expansion","text":"Entered a new Southeast Asian market.","source":"Demo company announcement"},{"date":"Aug 2026","type":"Leadership","text":"Appointed a new Chief People Officer.","source":"Demo company announcement"},{"date":"Jun 2026","type":"Funding","text":"Announced a Series C funding round.","source":"Demo company announcement"}]} if c.lower()=="acme technologies" else {"industry":"Not reliably identified","founded":"Not publicly verified","global_hq":"Not publicly verified","india_presence":"Not publicly verified","employees":"Not publicly verified","status":"Not publicly verified","description":"No reliable demo dataset available for this company.","signals":[]}
 gaps=["Current HRMS","Main HR challenge","Decision-maker","Budget","Buying timeline","Current vendor"];a=[]
 for x in s["signals"]:
  a.append({"title":x["type"]+" / business change","text":"Explore whether this change has created new HR or operational requirements.","basis":x["text"]})
 return {"company":c,"snapshot":s,"signals":s["signals"],"angles":a,"gaps":gaps,"questions":["What HR system are you currently using?","What prompted you to evaluate this now?","Which HR processes are hardest to manage?","Who else is involved in evaluating and approving a solution?","Has budget been allocated?","What is the decision or implementation timeline?"],"notice":"Demo mode: replace with verified web research before production."}
def has(t,terms): return any(x in t.lower() for x in terms)
def analyze(p):
 t=p.get("transcript","");c=p.get("company","Acme Technologies");r=p.get("research") or research(c)
 checks={"Need":["pain","problem","challenge","issue","need","struggle"],"Impact":["impact","cost","hours","time spent","saving","revenue","manual work"],"Budget":["budget","investment","spend","allocated","inr","₹"],"Authority":["decision maker","decision-maker","approve","approval","cfo","ceo","final decision","procurement"],"Timeline":["timeline","q1","q2","q3","q4","deadline","next month","next quarter"],"Current solution":["using","currently use","current hrms","workday","darwinbox","sap","oracle","bamboohr","keka"]}
 f=[{"category":k,"status":"established" if has(t,v) else "not_established","evidence":"Clear evidence was found in the transcript." if has(t,v) else "No clear evidence found in the transcript."} for k,v in checks.items()]
 d=[]
 if has(t,["darwinbox","workday","sap","oracle","keka","bamboohr"]):d.append("Current HR/business system was identified.")
 if has(t,["attendance","payroll","recruit","hiring","onboarding"]):d.append("A specific HR process was discussed.")
 if has(t,["demo","next step","follow up","follow-up","schedule"]):d.append("A next step was discussed.")
 if not d:d=["No structured discoveries were detected in this demo transcript."]
 m=[]
 if r["signals"] and not has(t,["expansion","locations","offices","geography","market"]):m.append("A verified growth/location signal was not explored.")
 if not has(t,checks["Authority"]):m.append("Decision-making authority was not established.")
 if not has(t,checks["Budget"]):m.append("Budget was not discussed.")
 if not has(t,checks["Impact"]):m.append("Business impact was not quantified.")
 a=[]
 for obj,q,terms in [("Establish decision process","Who else would be involved before you could move forward?",checks["Authority"]),("Quantify business impact","How much time, cost, or effort does the current problem create?",checks["Impact"]),("Understand commercial readiness","Has a budget been allocated or are you still evaluating the investment?",checks["Budget"]),("Establish timeline","Is there a specific decision or implementation date?",checks["Timeline"])]:
  if not has(t,terms):a.append({"priority":"HIGH" if len(a)<2 else "MEDIUM","objective":obj,"question":q})
 return {"company":c,"findings":f,"discovered":d,"missed":m,"next_actions":a,"already_established":[x["category"] for x in f if x["status"]=="established"]}
if __name__=="__main__":
 port=int(os.getenv("PORT","8000"));print("SDR MVP on",port);ThreadingHTTPServer(("0.0.0.0",port),H).serve_forever()
