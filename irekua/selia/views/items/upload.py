from django.shortcuts import render
from django import forms
from collections import defaultdict

from database import models
from database.formats import get_media_info
from database.formats import get_capture_date


def handle_files(files, sampling_event_device, user, licence):
    collection_type = sampling_event_device.sampling_event.collection.collection_type

    if collection_type.restrict_item_types:
        queryset = collection_type.item_types.all()
    else:
        queryset = models.ItemType.objects.all()  # pylint: disable=E1101

    errors = {}
    warnings = defaultdict(dict)
    success = []
    for tempfile in files:
        data = {
            'created_by': user,
            'item_file': tempfile,
            'sampling_event_device': sampling_event_device,
            'licence': licence,
        }
        possible_types = queryset.filter(media_type=tempfile.content_type)

        try:
            data['item_type'] = possible_types.get()
        except models.ItemType.MultipleObjectsReturned:  # pylint: disable=E1101
            data['item_type'] = None
            warnings[tempfile._name]['item_type'] = "Multiple possible item types for file"
        except models.ItemType.DoesNotExist:  # pylint: disable=E1101
            errors[tempfile._name] = "Does not have a valid mime/type for this collection"  # pylint: disable=W0212
            del warnings[tempfile._name]
            continue
        except Exception as error:
            errors[tempfile._name] = str(error)  # pylint: disable=W0212
            del warnings[tempfile._name]
            continue

        try:
            data['media_info'] = get_media_info(tempfile)
        except IOError as error:
            data['media_info'] = {}
            warnings[tempfile._name]['media_info'] = "An error was encountered while extracting media info %s" % str(error)
        except Exception as error:
            errors[tempfile._name] = str(error)  # pylint: disable=W0212
            del warnings[tempfile._name]
            continue

        try:
            data['captured_on'] = get_capture_date(tempfile)
        except IOError:
            data['captured_on'] = None
            warnings[tempfile._name]['captured_on'] = "No capture date was found"
        except Exception as error:
            errors[tempfile._name] = str(error)  # pylint: disable=W0212
            del warnings[tempfile._name]
            continue

        try:
            models.Item.objects.create(**data)
            success.append(tempfile._name)
        except Exception as error:
            errors[tempfile._name] = str(error)

    warnings = dict(warnings)

    return errors, warnings, success


def upload_items(request, collection_name, sampling_event_id, sampling_event_device_id):
    collection = models.Collection.objects.get(pk=collection_name)
    errors = None
    warnings = None
    success = None

    class FileFieldForm(forms.Form):
        file_field = forms.FileField(
            widget=forms.ClearableFileInput(attrs={'multiple': True}),
            required=False)
        licence = forms.ModelChoiceField(
            queryset=collection.licence_set.all())


    if request.method == "POST":
        form = FileFieldForm(request.POST)
        files = request.FILES.getlist('file_field')

        if form.is_valid():
            sampling_event_device = models.SamplingEventDevice.objects.get(
                pk=sampling_event_device_id)
            user = request.user

            errors, warnings, success = handle_files(
                files,
                sampling_event_device,
                user,
                form.cleaned_data['licence'])

    else:
        form = FileFieldForm()

    context = {
        'errors': errors,
        'warnings': warnings,
        'success': success,
        'form': form,
        'collection_name': collection_name,
        'sampling_event_id': sampling_event_id,
        'sampling_event_device_id': sampling_event_device_id
    }
    return render(request, 'selia/items/upload.html', context)
