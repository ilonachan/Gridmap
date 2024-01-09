package Utils;

import java.util.stream.Stream;

public class RonExporter {
  public String field(String name, Object content) {
    return name+":"+content;
  }
  public String str(Object text) {
    return "\""+text+"\"";
  }
  public String tuple(Object... elements) {
    return this.tuple(Stream.of(elements));
  }
  public String tuple(Iterable<Object> elements) {
    return this.tuple(Utils.iterToStream(elements, false));
  }
  public String tuple(Stream<Object> elements) {
    return "("+elements.map(Object::toString).reduce("", (String acc, String s) -> acc + s + ",")+")";
  }
  public String array(Object... elements){
    return this.array(Stream.of(elements));
  }
  public String array(Iterable<Object> elements) {
    return this.array(Utils.iterToStream(elements, false));
  }
  public String array(Stream<Object> elements) {
    return "["+elements.map(Object::toString).reduce("", (String acc, String s) -> acc + s + ",")+"]";
  }
  public String struct(Object... elements) {
    return this.struct(Stream.of(elements));
  }
  public String struct(Iterable<Object> elements) {
    return this.struct(Utils.iterToStream(elements, false));
  }
  public String struct(Stream<Object> elements) {
    return "{"+elements.map(Object::toString).reduce("", (String acc, String s) -> acc + s + ",")+"}";
  }
}