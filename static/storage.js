/* نظام حفظ المحادثات الدائم — Hussein Ghallab System */
var ChatStorage = (function(){
  var KEY = "hussein_ghallab_conversations_v1";
  var MAX_CONVS = 100;

  function load(){
    try {
      var raw = localStorage.getItem(KEY);
      return raw ? JSON.parse(raw) : { conversations: [], activeId: null };
    } catch(e) {
      return { conversations: [], activeId: null };
    }
  }

  function save(data){
    try {
      if(data.conversations.length > MAX_CONVS){
        data.conversations = data.conversations.slice(-MAX_CONVS);
      }
      localStorage.setItem(KEY, JSON.stringify(data));
    } catch(e) { console.warn("Storage full", e); }
  }

  function newId(){
    return "c_" + Date.now() + "_" + Math.random().toString(36).slice(2, 8);
  }

  return {
    list: function(){ return load().conversations; },
    getActiveId: function(){ return load().activeId; },
    setActive: function(id){
      var d = load(); d.activeId = id; save(d);
    },
    create: function(title){
      var d = load();
      var conv = {
        id: newId(),
        title: title || "محادثة " + new Date().toLocaleString("ar"),
        messages: [],
        createdAt: Date.now(),
        updatedAt: Date.now()
      };
      d.conversations.push(conv);
      d.activeId = conv.id;
      save(d);
      return conv;
    },
    get: function(id){
      var d = load();
      return d.conversations.find(function(c){ return c.id === id; }) || null;
    },
    addMessage: function(convId, role, content, provider){
      var d = load();
      var conv = d.conversations.find(function(c){ return c.id === convId; });
      if(!conv) return null;
      conv.messages.push({
        id: "m_" + Date.now() + "_" + Math.random().toString(36).slice(2,6),
        role: role,
        content: content,
        provider: provider || "",
        at: Date.now()
      });
      conv.updatedAt = Date.now();
      if(conv.messages.length === 1 && role === "user"){
        conv.title = content.slice(0, 40) + (content.length > 40 ? "..." : "");
      }
      save(d);
      return conv;
    },
    remove: function(id){
      var d = load();
      d.conversations = d.conversations.filter(function(c){ return c.id !== id; });
      if(d.activeId === id) d.activeId = null;
      save(d);
    },
    clearAll: function(){ save({ conversations: [], activeId: null }); },
    export: function(){ return JSON.stringify(load(), null, 2); },
    import: function(json){
      try {
        var data = JSON.parse(json);
        if(data.conversations) save(data);
        return true;
      } catch(e) { return false; }
    }
  };
})();
