/*
 * To change this template, choose Tools | Templates
 * and open the template in the editor.
 */

package util;
import java.io.*;
import java.util.zip.*;
/**
 * A class to read GZIP files, i.e. all files with extension
 * 'gz', or 'gzip'.
 * @author hendrik1
 */
public class GZipReader {
    /**flag indicating whether or
     * not the reader is opened*/
    private boolean isOpen;
    /**the GZIP file object*/
    private File zipFile;
    /**the reader object*/
    private BufferedReader reader;
    /**
     * Constructs a GZIP reader object, where the
     * argument <tt>zipFile</tt> is the absolute path
     * string of the GZIp file to read. <b>Note</b>, that
     * this constructor initializes a reader object thus
     * calling the {@link close() } method is crucial.
     * @param zipFile the absolute path of the file to read
     * @throws java.io.IOException an i/o error occurred
     */
    public GZipReader (String zipFile) throws IOException {
        this.zipFile = new File (zipFile);
        open();
    }
    /**
     * Constructs a GZIP reader object, where the
     * argument <tt>zipFile</tt> is a {@link File} instance 
     * representing the GZIp file to read. <b>Note</b>, that
     * this constructor initializes a reader object thus
     * calling the {@link close() } method is crucial.
     * @param zipFile the absolute path of the file to read
     * @throws java.io.IOException an i/o error occurred
     */
    public GZipReader (File zipFile) throws IOException {
        this.zipFile = zipFile;
        open();
    }
    /**
     * Closes the reader object
     * @throws java.io.IOException an i/o error occurred
     */
    public void close () throws IOException {
        isOpen = false;
        reader.close();
    }
    @Override
    protected void finalize () throws IOException {
        try{
            close();
        } finally {
            isOpen = false;
            reader.close();
        }
    }
    /**
     * Returns the absolute path of the GZIP file object
     * @return the absolute path
     */
    public String getGZipAbsolutePath (){
        return zipFile.getAbsolutePath();
    }
    /**
     * Returns the GZIP file name
     * @return the file name
     */
    public String getGZipName (){
        return zipFile.getName();
    }
    /**
     * Returns true if and only if the end of file
     * has been reached, i.e. <code>reader.readLine()==null</code>
     * returns true
     * @return true if EOF reached
     * @throws java.io.IOException an i/o error occurred
     */
    public boolean isEndOfFile () throws IOException {
        if (!isOpen) return false;
        return reader.readLine()==null?true:false;
    }
    /**
     * Returns true, if this reader object's open method was called
     * @return true if this object is opened
     */
    public boolean isOpen (){return isOpen;}
    /**
     * Opens the the reader object
     * @throws java.io.IOException an i/o error occurred
     */
    public void open () throws IOException {
        reader = new BufferedReader (new InputStreamReader (new GZIPInputStream (
                    new FileInputStream(zipFile))));
        isOpen = true;
    }
    /**
     * Returns the a string representation of each
     * line of the file to be read
     * @return the line string
     * @throws java.io.IOException
     */
    public String readLine () throws IOException {
        String s;
        return (s = reader.readLine())==null?null:s;
    }
    /**
     * Inner class to return a shallow copy of the
     * internal reader
     */
    protected class ReaderHandle {
        final BufferedReader readerH = reader;

        /**
         * Returns a shallow copy of the internal
         * reader object
         * @return a copy of the reader
         */
        protected BufferedReader getReaderHandle (){
            return readerH;
        }
    }
    public static void main (String[] args){
        try{
            GZipReader reader = new GZipReader("");
            GZipReader.ReaderHandle h = reader.new ReaderHandle();
            BufferedReader re = h.getReaderHandle();
            re.close();
            reader.close();
        } catch(IOException e){e.printStackTrace();}
    }
}
