import axios from "axios";
const FILE_UPLOAD_URL = "https://media.habitnetwork.xyz/uploadMediaFile/9";

const uploadImageFile = async (_blob) => {
  const formData = new FormData();
  formData.append("image", _blob, _blob.name ? _blob.name : "sign");
  formData.append("isResizeRequired", true);
  const data = await axios
    .post(FILE_UPLOAD_URL, formData, {
      headers: {
        "Content-Type": "multipart/form-data",
      },
    })
    .catch((e) => {
      console.log("error", e);
    });
  return data.data.mediaVariantDTOs[0].url;
};

export { uploadImageFile };
