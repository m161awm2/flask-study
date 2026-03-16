
const infoTitle = document.getElementById("infoTitle");
const infoDesc = document.getElementById("infoDesc");
const visualBox = document.getElementById("visualBox");
const infoTag = document.getElementById("infoTag");

const focusText = document.getElementById("focusText");
const envText = document.getElementById("envText");
const missionText = document.getElementById("missionText");

const menuButtons = document.querySelectorAll(".menu-btn");
const miniCards = document.querySelectorAll(".mini-card");
const clock = document.getElementById("clock");
const terminalLog = document.getElementById("terminalLog");

function updateClock() {
  if (!clock) return;

  const now = new Date();
  const hh = String(now.getHours()).padStart(2, "0");
  const mm = String(now.getMinutes()).padStart(2, "0");
  const ss = String(now.getSeconds()).padStart(2, "0");

  clock.textContent = `${hh}:${mm}:${ss}`;
}

function addTerminalLine(message) {
  if (!terminalLog) return;

  const line = document.createElement("div");
  const timestamp = new Date().toLocaleTimeString("ko-KR", {
    hour12: false,
  });

  line.innerHTML = `<span class="green">[${timestamp}]</span> ${message}`;
  terminalLog.appendChild(line);

  while (terminalLog.children.length > 12) {
    terminalLog.removeChild(terminalLog.firstChild);
  }
}

function updateInfoDetails(title, tag) {
  if (!focusText || !envText || !missionText) return;

  const titleText = (title || "").toUpperCase();

  if (titleText.includes("ABOUT") || tag === "IDENTITY") {
    focusText.textContent = "실습 중심 학습";
    envText.textContent = "Linux / Home Server";
    missionText.textContent = "배포와 운영 경험 축적";
    return;
  }

  if (titleText.includes("SKILL") || tag === "STACK") {
    focusText.textContent = "Linux / Nginx / Docker";
    envText.textContent = "CLI / Server / Network";
    missionText.textContent = "핵심 기술 스택 확장";
    return;
  }

  if (titleText.includes("PROJECT") || tag === "PROJECT") {
    focusText.textContent = "홈서버 운영";
    envText.textContent = "Nginx / External Access";
    missionText.textContent = "실제 서비스 감각 익히기";
    return;
  }

  if (titleText.includes("LINK") || tag === "LINK") {
    focusText.textContent = "외부 활동 연결";
    envText.textContent = "Velog / GitHub / Instagram";
    missionText.textContent = "기록과 결과물 통합";
    return;
  }

  if (titleText.includes("ROADMAP") || tag === "ROADMAP") {
    focusText.textContent = "Docker / Cloud / DevOps";
    envText.textContent = "확장형 학습 구조";
    missionText.textContent = "한 단계 더 실제에 가깝게";
    return;
  }

  if (tag === "OS") {
    focusText.textContent = "리눅스 기본기";
    envText.textContent = "Rocky Linux";
    missionText.textContent = "운영체제 이해도 강화";
    return;
  }

  if (tag === "WEB") {
    focusText.textContent = "웹서버 운영";
    envText.textContent = "Nginx";
    missionText.textContent = "서비스 구동 구조 이해";
    return;
  }

  if (tag === "ACCESS") {
    focusText.textContent = "원격 서버 관리";
    envText.textContent = "SSH";
    missionText.textContent = "실전 운영 흐름 익히기";
    return;
  }

  if (tag === "NETWORK") {
    focusText.textContent = "포트포워딩 / IP / 도메인";
    envText.textContent = "네트워크 구성";
    missionText.textContent = "외부 공개 구조 이해";
    return;
  }

  if (tag === "CONTAINER") {
    focusText.textContent = "컨테이너 기반 실행";
    envText.textContent = "Docker";
    missionText.textContent = "실행 환경 표준화";
    return;
  }

  if (tag === "CLOUD") {
    focusText.textContent = "클라우드 확장";
    envText.textContent = "AWS 등 클라우드 환경";
    missionText.textContent = "안정성과 확장성 경험";
    return;
  }

  focusText.textContent = "학습 중";
  envText.textContent = "실습 환경";
  missionText.textContent = "경험 축적";
}

function applyModuleData({ title, desc, visual, tag }) {
  if (infoTitle) infoTitle.textContent = title || "";
  if (infoDesc) infoDesc.textContent = desc || "";
  if (visualBox) visualBox.textContent = visual || "";
  if (infoTag) infoTag.textContent = tag || "MODULE";

  updateInfoDetails(title, tag);
  addTerminalLine(`[LOAD] ${title} module selected`);
}

menuButtons.forEach((button) => {
  button.addEventListener("click", () => {
    menuButtons.forEach((btn) => btn.classList.remove("active"));
    button.classList.add("active");

    applyModuleData({
      title: button.dataset.title,
      desc: button.dataset.desc,
      visual: button.dataset.visual,
      tag: button.dataset.tag,
    });
  });
});

miniCards.forEach((card) => {
  card.addEventListener("click", () => {
    applyModuleData({
      title: card.dataset.title,
      desc: card.dataset.desc,
      visual: card.dataset.visual,
      tag: card.dataset.tag,
    });
  });
});

updateClock();
setInterval(updateClock, 1000);

const rotatingLogs = [
  "[TRACE] monitoring interface state...",
  "[INFO] cyber panel stable",
  "[INFO] portfolio node active",
  "[CHECK] link routes available",
  "[TRACE] waiting for module input...",
  "[INFO] system glow normal",
];

let logIndex = 0;

setInterval(() => {
  addTerminalLine(rotatingLogs[logIndex]);
  logIndex = (logIndex + 1) % rotatingLogs.length;
}, 4000);
