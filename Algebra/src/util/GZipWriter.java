/*
 * To change this template, choose Tools | Templates
 * and open the template in the editor.
 */

package util;
import java.io.*;
import java.util.zip.*;
/**
 * A class providing functionality of GZip file
 * writing
 * @author hendrik1
 */
public class GZipWriter {
    /**the default line terminator*/
    public static final String LINE_TERMINATOR = "\n";
    /**the ouput file object*/
    private File output;
    /**the output stream object*/
    private BufferedOutputStream writer;
    /**
     * Constructs a <code>GZipWriter</code> object
     * where the argument <tt>path</tt> specifies the
     * output file path
     * @param path the output file path
     * @throws java.io.IOException an i/o error occurred
     */
    public GZipWriter (String path) throws IOException {
        open(new File(path));
    }
    /**
     * Constructs a <code>GZipWriter</code> object
     * where the argument <tt>output</tt> specifies the
     * output file
     * @param output the output file
     * @throws java.io.IOException an i/o error occurred
     */
    public GZipWriter (File output) throws IOException {
        open(output);
    }
    /**
     * Opens the output file stream to start writing
     * @param output the output file
     * @throws java.io.IOException an i/o error occurred
     */
    private void open (File output) throws IOException {
        this.output = output;
        writer = new BufferedOutputStream (new GZIPOutputStream (
                new FileOutputStream(output)));
    }
    /**
     * Closes the output stream
     * @throws java.io.IOException an i/o error occurred
     */
    public void close () throws IOException {
        writer.close();
    }
    /**
     * Flushes all data in the output stream
     * @throws java.io.IOException an i/o error occurred
     */
    public void flush()throws IOException {
        writer.flush();
    }
    /**
     * Returns the output file object
     * @return the output file
     */
    public File getOutputFile(){
        return output;
    }
    /**
     * Returns the output file path as a string
     * @return output file path
     */
    public String getOutputPath (){
        return output.getAbsolutePath();
    }
    /**
     * Writes the <code>CharSequence</code> object to
     * the output file
     * @param c the character sequence
     * @throws java.io.IOException an i/o error occurred
     */
    public void write (CharSequence c)throws IOException {
        for (int i = 0; i < c.length(); i++){
            writer.write((int) c.charAt(i));
        }
    }
    public static void main (String[] args){
        try{
            BufferedReader reader = new BufferedReader (new FileReader("C:/" +
                    "Dokumente und Einstellungen/hendrik1/Eigene Dateien/"+
                "DNA - Kram/DATEN_Andrade/refGene_protCoding4Gabriel.txt"));
            GZipWriter writer = new GZipWriter ("C:/" +
                    "Dokumente und Einstellungen/hendrik1/Eigene Dateien/"+
                "DNA - Kram/DATEN_Andrade/refGene_protCoding4Gabriel.txt.gz");
            String s;
            while ((s = reader.readLine())!=null){
                writer.write(s);
                writer.write(LINE_TERMINATOR);
            }
            reader.close();
            writer.close();
        } catch (IOException e){e.printStackTrace();}
    }
}
