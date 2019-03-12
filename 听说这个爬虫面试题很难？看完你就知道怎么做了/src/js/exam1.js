const jsdom = require("jsdom");
const { JSDOM } = jsdom;

function get_css(html){
    const dom = new JSDOM(html);
    window = dom.window;
    document = window.document;
    window.decodeURIComponent = decodeURIComponent;

    let script_element = document.querySelector("script");
    let script = script_element.innerHTML;
    eval(script);
    return Buffer.from(window.document.querySelector("style").sheet.toString()).toString("base64");
}
