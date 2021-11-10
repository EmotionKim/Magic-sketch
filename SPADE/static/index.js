currentSize = 5;
var currentColor = "#759edf";
var myBoard = new DrawingBoard.Board("zbeubeu", {
  controls: [
    { Size: { type: "dropdown" } },
    "DrawingMode",
    "Navigation",
    "Download"
  ]
});

myBoard.clearWebStorage();


jQuery(document).ready(function($) {
  $color_list = [
    { color: "#384f83", title: "sea" },
    { color: "#efefef", title: "cloud" },
    { color: "#2c1e16", title: "dirt" },
    { color: "#5d6e32", title: "bush" },
    { color: "#b7d24e", title: "grass" },
    { color: "#3c3b4b", title: "mountain" },
    { color: "#987e6a", title: "road" },
    { color: "#759edf", title: "sky-other" },
    { color: "#352613", title: "tree" },
    { color: "#636363", title: "pavement" },
    { color: "#e670b6", title: "flower" },
    { color: "#c1c3c9", title: "fog" },
    { color: "#776c2d", title: "hill" },
    { color: "#bf602c", title: "leaves" },
    { color: "#32604d", title: "river" },
    { color: "#fafafa", title: "snow" },
    { color: "#7CFC00", title: "airplane" },
    { color: "#D2D2D2", title: "boat" },
    { color: "#D2691E", title: "bridge" },
    { color: "#8B0000", title: "roof*" },
    { color: "#DEB887", title: "house*" },
    { color: "#00CED1", title: "window-other*" },
    { color: "#B22222", title: "wall-brick*" },
    { color: "#8B4513", title: "branch" }
  ];

  $(".color-picker").wrap('<div class="color-picker-wrap"></div>');

  $(".color-picker-wrap").each(function() {
    var self = $(this);

    if (self.children(".color-picker").hasClass("cp-sm")) {
      self.addClass("cp-sm");
    } else if (self.children(".color-picker").hasClass("cp-lg")) {
      self.addClass("cp-lg");
    }

    self.append('<ul></ul><input type="color" style="display:none;" />');

    var $foundactive = false;

    for (var i = 0; i < $color_list.length; i++) {
      var $active = "";

      if (self.children(".color-picker").val() == $color_list[i].color) {
        $active = 'class="active"';

        $foundactive = true;
      }

      self
        .children("ul")
        .append(
          "<li " +
            $active +
            ' style="background-color:' +
            $color_list[i].color +
            '" title="' +
            $color_list[i].title +
            '">&nbsp&nbsp' +
            $color_list[i].title +
            "&nbsp&nbsp</li>"
        );
    }

    if (!$foundactive && self.children(".color-picker").val() != "") {
      self
        .children("ul")
        .append(
          '<li class="active" title="Custom Color ' +
            self.children(".color-picker").val() +
            '" style="background-color:' +
            self.children(".color-picker").val() +
            '"></li>'
        );

      if (self.children(".color-picker").hasClass("cp-show")) {
        self.children("small").remove();

        self.append(
          "<small>Selected Color: <code>" +
            self.children(".color-picker").val() +
            "</code></small>"
        );
      }
    }
  });

  $(".color-picker-wrap ul").on("click", "li", function() {
    console.log("1");

    var self = $(this);

    if (!self.hasClass("active")) {
      self.siblings().removeClass("active");

      var color = self.css("backgroundColor");

      console.log(color);

      currentColor = color;
      myBoard.ctx.strokeStyle = color;

      self
        .parents(".color-picker-wrap")
        .children(".color-picker")
        .val(color);

      self.addClass("active");
    }
  });

  $(".color-picker-wrap input[type='color']").on("change", function() {
    var self = $(this);

    self
      .parents(".color-picker-wrap")
      .children("ul")
      .children("li")
      .removeClass("active");

    self
      .parents(".color-picker-wrap")
      .children("ul")
      .append(
        '<li class="active" title="Custom Color ' +
          self.val() +
          '" style="background-color:' +
          self.val() +
          '"></li>'
      );

    self
      .parents(".color-picker-wrap")
      .children(".color-picker")
      .val(self.val());

    if (
      self
        .parents(".color-picker-wrap")
        .children(".color-picker")
        .hasClass("cp-show")
    ) {
      self
        .parents(".color-picker-wrap")
        .children("small")
        .remove();

      self
        .parents(".color-picker-wrap")
        .append(
          "<small>Selected Color: <code>" + self.val() + "</code></small>"
        );
    }
  });
});

document.getElementById("uploadimage").addEventListener(
  "click",
  function() {
    upload("canvas");
  },
  false
);

function upload(canvas) {
  var dataURL = myBoard.getImg();
  console.log(dataURL);
  let img = document.getElementById("image");
  img.src = "/img/loading.gif";

  fetch("/upload", {
    method: "POST",
    body: dataURL
  })
    .then(response => response.json())
    .then(r => {
      let x = r.location;
      let img = document.getElementById("image");
      console.log("img", img.src);
      img.src = "/" + x;
      console.log(img.src);
    });
}

console.log(myBoard.color);
