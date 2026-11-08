// Keystroke savings on held-out UD test sentences (3 suggestions, the target word chosen as soon as it appears).
// Usage: N=100 node keystroke_savings.js <lang> <ud-test.conllu> [learn]  (LEX=dir that holds lex/, default the repo root)
const fs=require('fs');const KP=require(__dirname+'/../patch-0.7.0/predict.js');
const [lang,file,learnFlag,countArg]=process.argv.slice(2);const COUNT=+(countArg||3);
global.fetch=async p=>({ok:true,json:async()=>JSON.parse(fs.readFileSync((process.env.LEX||__dirname+'/../../')+p))});
(async()=>{await KP.load(lang);
 const sents=[];let cur=[];for(const line of fs.readFileSync(file,'utf8').split('\n')){if(line.startsWith('# text = ')){sents.push(line.slice(9));}}
 const model=KP.emptyModel();let base=0,cost=0,t0=Date.now(),calls=0;
 for(const s of sents.slice(0,+(process.env.N||200))){
  const words=s.split(/\s+/).filter(Boolean);let text='';
  for(const w of words){
   const bare=w.match(/^(.*?)([.,;:!?»")]*)$/u);const core=bare[1],punct=bare[2];
   base+=[...w].length+1;
   let typed=0;const chars=[...core];let done=false;
   while(typed<chars.length){
    const cand=/[\p{L}]/u.test(core)?KP.suggest({text,cursor:text.length,lang,model,count:COUNT}):[];calls++;
    const hit=cand.find(c=>c.value.toLowerCase()===text.slice(cand[0]?.start||0).toLowerCase()+chars.slice(typed).join('').toLowerCase()&&false);
    const target=core.slice(chars.slice(0,typed).join('').length);
    const ok=cand.find(c=>{const already=text.slice(c.start);return (c.value).toLowerCase()===(already+target).toLowerCase();});
    if(ok){cost+=1;text=text.slice(0,ok.start)+ok.value+(punct?'':' ');if(punct){text+=punct+' ';cost+=[...punct].length;}else{} done=true;break;}
    text+=chars[typed];typed++;cost++;
   }
   if(!done){text+=punct+' ';cost+=[...punct].length+1;}
  }
  if(learnFlag==='learn')KP.learn(model,lang,s);
 }
 console.log(lang,'sentences',Math.min(+(process.env.N||200),sents.length),'KS',(100*(1-cost/base)).toFixed(1)+'%','ms/call',((Date.now()-t0)/calls).toFixed(2));
})();
