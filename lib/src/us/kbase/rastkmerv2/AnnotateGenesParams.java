
package us.kbase.rastkmerv2;

import java.util.HashMap;
import java.util.Map;
import javax.annotation.Generated;
import com.fasterxml.jackson.annotation.JsonAnyGetter;
import com.fasterxml.jackson.annotation.JsonAnySetter;
import com.fasterxml.jackson.annotation.JsonInclude;
import com.fasterxml.jackson.annotation.JsonProperty;
import com.fasterxml.jackson.annotation.JsonPropertyOrder;


/**
 * <p>Original spec-file type: AnnotateGenesParams</p>
 * 
 * 
 */
@JsonInclude(JsonInclude.Include.NON_NULL)
@Generated("com.googlecode.jsonschema2pojo")
@JsonPropertyOrder({
    "input_genome_ref",
    "output_workspace",
    "output_genome_name"
})
public class AnnotateGenesParams {

    @JsonProperty("input_genome_ref")
    private String inputGenomeRef;
    @JsonProperty("output_workspace")
    private String outputWorkspace;
    @JsonProperty("output_genome_name")
    private String outputGenomeName;
    private Map<String, Object> additionalProperties = new HashMap<String, Object>();

    @JsonProperty("input_genome_ref")
    public String getInputGenomeRef() {
        return inputGenomeRef;
    }

    @JsonProperty("input_genome_ref")
    public void setInputGenomeRef(String inputGenomeRef) {
        this.inputGenomeRef = inputGenomeRef;
    }

    public AnnotateGenesParams withInputGenomeRef(String inputGenomeRef) {
        this.inputGenomeRef = inputGenomeRef;
        return this;
    }

    @JsonProperty("output_workspace")
    public String getOutputWorkspace() {
        return outputWorkspace;
    }

    @JsonProperty("output_workspace")
    public void setOutputWorkspace(String outputWorkspace) {
        this.outputWorkspace = outputWorkspace;
    }

    public AnnotateGenesParams withOutputWorkspace(String outputWorkspace) {
        this.outputWorkspace = outputWorkspace;
        return this;
    }

    @JsonProperty("output_genome_name")
    public String getOutputGenomeName() {
        return outputGenomeName;
    }

    @JsonProperty("output_genome_name")
    public void setOutputGenomeName(String outputGenomeName) {
        this.outputGenomeName = outputGenomeName;
    }

    public AnnotateGenesParams withOutputGenomeName(String outputGenomeName) {
        this.outputGenomeName = outputGenomeName;
        return this;
    }

    @JsonAnyGetter
    public Map<String, Object> getAdditionalProperties() {
        return this.additionalProperties;
    }

    @JsonAnySetter
    public void setAdditionalProperties(String name, Object value) {
        this.additionalProperties.put(name, value);
    }

    @Override
    public String toString() {
        return ((((((((("AnnotateGenesParams"+" [inputGenomeRef=")+ inputGenomeRef)+", outputWorkspace=")+ outputWorkspace)+", outputGenomeName=")+ outputGenomeName)+", additionalProperties=")+ additionalProperties)+"]");
    }

}
