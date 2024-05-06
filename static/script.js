class BoggleGame {
  constructor(boardNo, secs = 60) {
    this.secs = secs;
    this.showRemaingTime();
    this.score = 0;
    this.words = new Set();
    this.board = $("#" + boardNo);

    this.timer = setInterval(this.tickDown.bind(this), 1000);

    $(".guessed-word", this.board).on("submit", this.handleSubmit.bind(this));
  }

  /*-- show words as they're guess */
  showWord(guess) {
    $(".guessed-words", this.board).append($("<li>", { text: guess }));
  }

  /* Handle Score Display */
  showScore() {
    $(".score", this.board).text(this.score);
  }

  /*Handle Staus Message */
  showStausMessage(msg, cls) {
    $(".msg", this.board).text(msg).removeClass().addClass(`msg ${cls}`);
  }

  /* Word Submission */

  async handleSubmit(evt) {
    evt.preventDefault();
    const $word = $(".guess", this.board);
    console.log($word);

    let guess = $word.val();
    if (!guess) return;

    if (this.words.has(guess)) {
      this.showStausMessage(`Already found ${guess}`, "error");
      return;
    }

    const resp = await axios.get("/submit-guess", { params: { guess: guess } });
    /**Filter out invalid words first*/
    if (resp.data.result === "not-word") {
      this.showStausMessage(
        `${word} is not in the current dictionary`,
        "error"
      );
    } else if (resp.data.result === "not-on-board") {
      this.showStausMessage(`${guess} is not on this board`, "error");
    } else {
      this.showWord(guess);
      this.score += guess.length;
      this.showScore();
      this.words.add(guess);
      this.showStausMessage(`${guess} is on the board!`, "good");
    }

    $word.val("").focus();
  }

  /* timer display */

  showRemaingTime() {
    $(".timer", this.board).text(this.secs);
  }

  /* Reduce Time Remaing */

  async tickDown() {
    this.secs -= 1;
    this.showRemaingTime();

    if (this.secs === 0) {
      clearInterval(this.timer);
      await this.gameEnd();
    }
  }

  /*game over */
  async scoreGame() {
    $(".guessed-word", this.board).hide();
    const resp = await axios.post("/score-submit", { score: this.score });
    if (resp.data.newRecord) {
      this.showStausMessage(`New Record: ${this.score}`, "good");
    } else {
      this.showStausMessage(`Final Score: ${this.score}`, "good");
    }
  }
}
